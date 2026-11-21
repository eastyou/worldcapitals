"""render 模块的单元测试。"""

from __future__ import annotations

import unittest

from worldcapitals.model import all_countries, quiz_items
from worldcapitals.render import match_html, quiz_html, table_html


class CommonMarkupTests(unittest.TestCase):
    def test_quiz_is_html_document(self) -> None:
        document = quiz_html(quiz_items(2, seed=1), "测试标题")
        self.assertTrue(document.startswith("<!DOCTYPE html>"))
        self.assertIn('lang="zh-CN"', document)
        self.assertIn('charset="utf-8"', document)

    def test_print_style_present(self) -> None:
        document = table_html(all_countries(), "总表")
        self.assertIn("@media print", document)
        self.assertIn("size: A4", document)

    def test_match_is_html_document(self) -> None:
        document = match_html([("中国", "北京")], "配对")
        self.assertTrue(document.startswith("<!DOCTYPE html>"))


class QuizHtmlTests(unittest.TestCase):
    def test_renders_questions_and_options(self) -> None:
        items = quiz_items(3, seed=5)
        document = quiz_html(items, "首都小测")
        for item in items:
            self.assertIn(str(item["question"]), document)
            for option in item["options"]:
                self.assertIn(str(option), document)

    def test_option_letters(self) -> None:
        document = quiz_html(quiz_items(1, seed=1), "首都小测")
        for letter in ("A", "B", "C", "D"):
            self.assertIn('class="letter">%s<' % letter, document)

    def test_with_answers_adds_key(self) -> None:
        items = quiz_items(2, seed=2)
        document = quiz_html(items, "带答案", with_answers=True)
        self.assertIn("参考答案", document)
        for item in items:
            self.assertIn(str(item["answer"]), document)

    def test_without_answers_has_no_key(self) -> None:
        document = quiz_html(quiz_items(2, seed=2), "无答案")
        self.assertNotIn("参考答案", document)

    def test_title_is_escaped(self) -> None:
        document = quiz_html([], '<script>alert("x")</script>')
        self.assertIn("&lt;script&gt;", document)
        self.assertNotIn("<script>alert", document)

    def test_question_text_is_escaped(self) -> None:
        item = {
            "question": "<b>哪座城市</b>？",
            "options": ["<i>甲</i>", "乙", "丙", "丁"],
            "answer": "<i>甲</i>",
        }
        document = quiz_html([item], "转义")
        self.assertIn("&lt;b&gt;", document)
        self.assertIn("&lt;i&gt;甲&lt;/i&gt;", document)
        self.assertNotIn("<b>哪座城市</b>", document)

    def test_empty_items_show_message(self) -> None:
        document = quiz_html([], "空卷")
        self.assertIn("暂无题目", document)

    def test_items_must_be_list(self) -> None:
        with self.assertRaises(TypeError):
            quiz_html("not-a-list", "错误")  # type: ignore[arg-type]

    def test_item_must_be_dict(self) -> None:
        with self.assertRaises(TypeError):
            quiz_html(["bad"], "错误")  # type: ignore[list-item]

    def test_missing_field_raises(self) -> None:
        with self.assertRaises(ValueError):
            quiz_html([{"question": "题目", "options": ["甲", "乙"]}], "缺字段")

    def test_answer_must_be_in_options(self) -> None:
        item = {"question": "题目", "options": ["甲", "乙"], "answer": "丙"}
        with self.assertRaises(ValueError):
            quiz_html([item], "答案错误")

    def test_duplicate_options_raise(self) -> None:
        item = {"question": "题目", "options": ["甲", "甲", "乙"], "answer": "甲"}
        with self.assertRaises(ValueError):
            quiz_html([item], "重复选项")

    def test_options_must_be_sequence(self) -> None:
        item = {"question": "题目", "options": "甲乙", "answer": "甲"}
        with self.assertRaises(TypeError):
            quiz_html([item], "选项错误")

    def test_too_few_options_raise(self) -> None:
        item = {"question": "题目", "options": ["甲"], "answer": "甲"}
        with self.assertRaises(ValueError):
            quiz_html([item], "选项不足")

    def test_with_answers_must_be_bool(self) -> None:
        with self.assertRaises(TypeError):
            quiz_html([], "类型错误", "yes")  # type: ignore[arg-type]


class MatchHtmlTests(unittest.TestCase):
    def test_renders_both_columns(self) -> None:
        pairs = [("中国", "北京"), ("日本", "东京")]
        document = match_html(pairs, "配对练习")
        self.assertIn("中国", document)
        self.assertIn("北京", document)
        self.assertIn("日本", document)
        self.assertIn("东京", document)
        self.assertIn("配对", document)

    def test_capitals_use_letters(self) -> None:
        document = match_html([("中国", "北京"), ("日本", "东京")], "配对")
        self.assertIn('class="letter">A<', document)
        self.assertIn('class="letter">B<', document)

    def test_text_is_escaped(self) -> None:
        document = match_html([("<国>", "<都>")], "<标题>")
        self.assertIn("&lt;国&gt;", document)
        self.assertIn("&lt;都&gt;", document)
        self.assertNotIn("<标题>", document)

    def test_empty_pairs_show_message(self) -> None:
        document = match_html([], "空配对")
        self.assertIn("暂无配对题目", document)

    def test_pairs_must_be_list(self) -> None:
        with self.assertRaises(TypeError):
            match_html("bad", "错误")  # type: ignore[arg-type]

    def test_pair_must_be_two_items(self) -> None:
        with self.assertRaises(ValueError):
            match_html([("中国",)], "错误")  # type: ignore[list-item]

    def test_pair_element_must_be_string(self) -> None:
        with self.assertRaises(TypeError):
            match_html([("中国", 1)], "错误")  # type: ignore[list-item]

    def test_pair_container_must_be_sequence(self) -> None:
        with self.assertRaises(TypeError):
            match_html([1], "错误")  # type: ignore[list-item]


class TableHtmlTests(unittest.TestCase):
    def test_groups_by_continent(self) -> None:
        document = table_html(all_countries(), "总表")
        self.assertIn("<h2>亚洲（15）</h2>", document)
        self.assertIn("<h2>欧洲（15）</h2>", document)
        self.assertIn("<h2>非洲（12）</h2>", document)
        self.assertIn("<h2>北美洲（10）</h2>", document)
        self.assertIn("<h2>南美洲（8）</h2>", document)
        self.assertIn("<h2>大洋洲（5）</h2>", document)

    def test_continent_order(self) -> None:
        document = table_html(all_countries(), "总表")
        positions = [document.index("<h2>%s" % name) for name in (
            "亚洲",
            "欧洲",
            "非洲",
            "北美洲",
            "南美洲",
            "大洋洲",
        )]
        self.assertEqual(positions, sorted(positions))

    def test_contains_country_and_capital(self) -> None:
        document = table_html(all_countries(), "总表")
        self.assertIn("中国", document)
        self.assertIn("北京", document)
        self.assertIn("Beijing", document)

    def test_title_is_escaped(self) -> None:
        document = table_html([], "<总表>")
        self.assertIn("&lt;总表&gt;", document)
        self.assertNotIn("<总表>", document)

    def test_empty_list_show_message(self) -> None:
        document = table_html([], "空表")
        self.assertIn("暂无国家数据", document)

    def test_items_must_be_country_objects(self) -> None:
        with self.assertRaises(TypeError):
            table_html(["中国"], "错误")  # type: ignore[list-item]

    def test_countries_must_be_list(self) -> None:
        with self.assertRaises(TypeError):
            table_html("bad", "错误")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
