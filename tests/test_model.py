"""model 模块的单元测试。"""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from worldcapitals.model import (
    CONTINENTS,
    Country,
    all_countries,
    capital_of,
    country_of,
    list_by_continent,
    match_items,
    normalize,
    quiz_items,
)


class AllCountriesTests(unittest.TestCase):
    def test_count_at_least_sixty(self) -> None:
        self.assertGreaterEqual(len(all_countries()), 60)

    def test_continent_distribution(self) -> None:
        counts = {}
        for country in all_countries():
            counts[country.continent] = counts.get(country.continent, 0) + 1
        self.assertEqual(counts["亚洲"], 15)
        self.assertEqual(counts["欧洲"], 15)
        self.assertEqual(counts["非洲"], 12)
        self.assertEqual(counts["北美洲"], 10)
        self.assertEqual(counts["南美洲"], 8)
        self.assertEqual(counts["大洋洲"], 5)

    def test_all_six_continents_present(self) -> None:
        present = {country.continent for country in all_countries()}
        self.assertEqual(present, set(CONTINENTS))

    def test_fields_are_non_empty(self) -> None:
        for country in all_countries():
            for value in (
                country.country_zh,
                country.country_en,
                country.capital_zh,
                country.capital_en,
                country.continent,
            ):
                self.assertIsInstance(value, str)
                self.assertTrue(value.strip())

    def test_aliases_are_tuple(self) -> None:
        for country in all_countries():
            self.assertIsInstance(country.aliases, tuple)

    def test_country_is_frozen(self) -> None:
        country = all_countries()[0]
        with self.assertRaises(FrozenInstanceError):
            country.country_zh = "测试"

    def test_country_names_unique(self) -> None:
        names = [country.country_zh for country in all_countries()]
        self.assertEqual(len(names), len(set(names)))

    def test_capital_names_unique(self) -> None:
        capitals = [country.capital_zh for country in all_countries()]
        self.assertEqual(len(capitals), len(set(capitals)))

    def test_returns_independent_copy(self) -> None:
        first = all_countries()
        first.clear()
        self.assertGreaterEqual(len(all_countries()), 60)

    def test_manual_country_construction(self) -> None:
        country = Country("测试国", "Testland", "测试城", "Testville", "亚洲", ("测试",))
        self.assertEqual(country.aliases, ("测试",))
        self.assertEqual(country.capital_zh, "测试城")


class NormalizeTests(unittest.TestCase):
    def test_strips_whitespace(self) -> None:
        self.assertEqual(normalize("  日本  "), "日本")

    def test_collapses_internal_whitespace(self) -> None:
        self.assertEqual(normalize("South   Korea"), "south korea")

    def test_casefolds_english(self) -> None:
        self.assertEqual(normalize("UNITED STATES"), "united states")

    def test_keeps_chinese(self) -> None:
        self.assertEqual(normalize("中华人民共和国"), "中华人民共和国")

    def test_empty_string(self) -> None:
        self.assertEqual(normalize("   "), "")

    def test_non_string_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            normalize(None)  # type: ignore[arg-type]


class CapitalOfTests(unittest.TestCase):
    def test_chinese_country(self) -> None:
        self.assertEqual(capital_of("日本"), "东京")

    def test_english_country(self) -> None:
        self.assertEqual(capital_of("Japan"), "东京")

    def test_english_is_case_insensitive(self) -> None:
        self.assertEqual(capital_of("jApAn"), "东京")

    def test_internal_spaces_are_normalized(self) -> None:
        self.assertEqual(capital_of("  South   Korea "), "首尔")

    def test_alias_usa(self) -> None:
        self.assertEqual(capital_of("USA"), "华盛顿")

    def test_alias_uk(self) -> None:
        self.assertEqual(capital_of("UK"), "伦敦")

    def test_alias_saudi(self) -> None:
        self.assertEqual(capital_of("沙特"), "利雅得")

    def test_self_named_capital(self) -> None:
        self.assertEqual(capital_of("新加坡"), "新加坡")

    def test_empty_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as caught:
            capital_of("   ")
        self.assertIn("65", str(caught.exception))

    def test_unknown_country_raises(self) -> None:
        with self.assertRaises(ValueError) as caught:
            capital_of("火星")
        message = str(caught.exception)
        self.assertIn("火星", message)
        self.assertIn("65", message)

    def test_non_string_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            capital_of(123)  # type: ignore[arg-type]


class CountryOfTests(unittest.TestCase):
    def test_chinese_capital(self) -> None:
        self.assertEqual(country_of("东京"), "日本")

    def test_english_capital(self) -> None:
        self.assertEqual(country_of("Tokyo"), "日本")

    def test_english_capital_case_insensitive(self) -> None:
        self.assertEqual(country_of("TOKYO"), "日本")

    def test_washington_dc(self) -> None:
        self.assertEqual(country_of("Washington, D.C."), "美国")

    def test_empty_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as caught:
            country_of("")
        self.assertIn("65", str(caught.exception))

    def test_unknown_capital_raises(self) -> None:
        with self.assertRaises(ValueError) as caught:
            country_of("亚特兰蒂斯")
        self.assertIn("亚特兰蒂斯", str(caught.exception))

    def test_non_string_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            country_of(None)  # type: ignore[arg-type]


class ListByContinentTests(unittest.TestCase):
    def test_chinese_name(self) -> None:
        self.assertEqual(len(list_by_continent("亚洲")), 15)

    def test_chinese_suffix(self) -> None:
        self.assertEqual(len(list_by_continent("亚洲国家")), 15)

    def test_english_name(self) -> None:
        self.assertEqual(len(list_by_continent("asia")), 15)

    def test_english_uppercase(self) -> None:
        self.assertEqual(len(list_by_continent("EUROPE")), 15)

    def test_north_america(self) -> None:
        self.assertEqual(len(list_by_continent("north america")), 10)

    def test_south_america_alias(self) -> None:
        self.assertEqual(len(list_by_continent("南美")), 8)

    def test_oceania(self) -> None:
        self.assertEqual(len(list_by_continent("oceania")), 5)

    def test_unknown_continent_lists_all_options(self) -> None:
        with self.assertRaises(ValueError) as caught:
            list_by_continent("南极洲")
        message = str(caught.exception)
        for continent in CONTINENTS:
            self.assertIn(continent, message)

    def test_empty_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            list_by_continent("  ")

    def test_non_string_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            list_by_continent(1)  # type: ignore[arg-type]

    def test_all_lists_sum_to_total(self) -> None:
        total = sum(len(list_by_continent(name)) for name in CONTINENTS)
        self.assertEqual(total, len(all_countries()))


class QuizTests(unittest.TestCase):
    def test_minimum_count(self) -> None:
        self.assertEqual(len(quiz_items(1)), 1)

    def test_maximum_count(self) -> None:
        self.assertEqual(len(quiz_items(40)), 40)

    def test_zero_count_raises(self) -> None:
        with self.assertRaises(ValueError):
            quiz_items(0)

    def test_count_over_limit_raises(self) -> None:
        with self.assertRaises(ValueError):
            quiz_items(41)

    def test_bool_count_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            quiz_items(True)  # type: ignore[arg-type]

    def test_string_count_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            quiz_items("10")  # type: ignore[arg-type]

    def test_item_shape(self) -> None:
        expected = {
            "country_zh",
            "country_en",
            "continent",
            "question",
            "options",
            "answer",
        }
        for item in quiz_items(5, seed=3):
            self.assertEqual(set(item.keys()), expected)

    def test_four_unique_options(self) -> None:
        for item in quiz_items(20, seed=7):
            options = item["options"]
            self.assertIsInstance(options, list)
            assert isinstance(options, list)
            self.assertEqual(len(options), 4)
            self.assertEqual(len(set(options)), 4)

    def test_answer_is_one_of_options(self) -> None:
        for item in quiz_items(20, seed=4):
            self.assertIn(item["answer"], item["options"])

    def test_seed_is_reproducible(self) -> None:
        self.assertEqual(quiz_items(10, seed=5), quiz_items(10, seed=5))

    def test_different_seeds_differ(self) -> None:
        self.assertNotEqual(quiz_items(40, seed=1), quiz_items(40, seed=2))

    def test_question_mentions_country(self) -> None:
        for item in quiz_items(6, seed=2):
            self.assertIn(str(item["country_zh"]), str(item["question"]))
            self.assertIn("首都是", str(item["question"]))

    def test_continent_filter(self) -> None:
        items = quiz_items(10, seed=1, continent="亚洲")
        for item in items:
            self.assertEqual(item["continent"], "亚洲")

    def test_continent_exact_capacity(self) -> None:
        items = quiz_items(5, seed=2, continent="大洋洲")
        self.assertEqual(len(items), 5)
        for item in items:
            options = item["options"]
            assert isinstance(options, list)
            self.assertEqual(len(set(options)), 4)

    def test_continent_too_small_raises(self) -> None:
        with self.assertRaises(ValueError) as caught:
            quiz_items(6, continent="大洋洲")
        self.assertIn("大洋洲", str(caught.exception))

    def test_unknown_continent_raises(self) -> None:
        with self.assertRaises(ValueError):
            quiz_items(5, continent="南极洲")

    def test_non_string_continent_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            quiz_items(5, continent=1)  # type: ignore[arg-type]

    def test_seed_none_allowed(self) -> None:
        self.assertEqual(len(quiz_items(3, seed=None)), 3)

    def test_seed_string_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            quiz_items(3, seed="5")  # type: ignore[arg-type]

    def test_seed_bool_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            quiz_items(3, seed=False)

    def test_negative_seed_allowed(self) -> None:
        self.assertEqual(quiz_items(4, seed=-9), quiz_items(4, seed=-9))


class MatchTests(unittest.TestCase):
    def test_minimum_count(self) -> None:
        self.assertEqual(len(match_items(1)), 1)

    def test_maximum_count(self) -> None:
        self.assertEqual(len(match_items(20)), 20)

    def test_zero_count_raises(self) -> None:
        with self.assertRaises(ValueError):
            match_items(0)

    def test_count_over_limit_raises(self) -> None:
        with self.assertRaises(ValueError):
            match_items(21)

    def test_bool_count_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            match_items(True)  # type: ignore[arg-type]

    def test_string_count_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            match_items("5")  # type: ignore[arg-type]

    def test_seed_is_reproducible(self) -> None:
        self.assertEqual(match_items(8, seed=11), match_items(8, seed=11))

    def test_pairs_are_unique(self) -> None:
        pairs = match_items(20, seed=6)
        self.assertEqual(len({country for country, _ in pairs}), 20)

    def test_pair_structure(self) -> None:
        for pair in match_items(10, seed=1):
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
            self.assertTrue(pair[0])
            self.assertTrue(pair[1])

    def test_seed_none_allowed(self) -> None:
        self.assertEqual(len(match_items(4, seed=None)), 4)

    def test_bad_seed_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            match_items(4, seed="abc")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
