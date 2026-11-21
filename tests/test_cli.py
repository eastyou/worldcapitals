"""cli 模块的单元测试。"""

from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from typing import Sequence, Tuple
from unittest import mock

from worldcapitals.cli import _ensure_utf8_console, main


class CliTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmpdir = self._tmp.name

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(self, argv: Sequence[str]) -> Tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def output_path(self, name: str) -> str:
        return os.path.join(self.tmpdir, name)


class HelpTests(CliTestCase):
    def test_no_args_shows_usage(self) -> None:
        code, out, err = self.run_cli([])
        self.assertEqual(code, 0)
        self.assertIn("用法", out)
        self.assertEqual(err, "")

    def test_help_flag(self) -> None:
        code, out, _err = self.run_cli(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("worldcapitals", out)

    def test_help_word(self) -> None:
        code, out, _err = self.run_cli(["help"])
        self.assertEqual(code, 0)
        self.assertIn("quiz", out)


class QueryTests(CliTestCase):
    def test_capital_chinese(self) -> None:
        code, out, err = self.run_cli(["capital", "日本"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "东京")
        self.assertEqual(err, "")

    def test_capital_alias(self) -> None:
        code, out, _err = self.run_cli(["capital", "USA"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "华盛顿")

    def test_capital_multiword_country(self) -> None:
        code, out, _err = self.run_cli(["capital", "South", "Korea"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "首尔")

    def test_capital_unknown(self) -> None:
        code, out, err = self.run_cli(["capital", "火星"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("错误：", err)
        self.assertIn("未知国家", err)

    def test_capital_missing_argument(self) -> None:
        code, _out, err = self.run_cli(["capital"])
        self.assertEqual(code, 2)
        self.assertIn("缺少国家名称", err)

    def test_capital_blank_argument(self) -> None:
        code, _out, err = self.run_cli(["capital", "   "])
        self.assertEqual(code, 2)
        self.assertIn("不能为空", err)

    def test_country_chinese(self) -> None:
        code, out, _err = self.run_cli(["country", "东京"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "日本")

    def test_country_english(self) -> None:
        code, out, _err = self.run_cli(["country", "tokyo"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "日本")

    def test_country_unknown(self) -> None:
        code, _out, err = self.run_cli(["country", "不存在"])
        self.assertEqual(code, 2)
        self.assertIn("未知首都", err)

    def test_country_missing_argument(self) -> None:
        code, _out, err = self.run_cli(["country"])
        self.assertEqual(code, 2)
        self.assertIn("缺少首都名称", err)


class ListTests(CliTestCase):
    def test_list_asia(self) -> None:
        code, out, _err = self.run_cli(["list", "亚洲"])
        self.assertEqual(code, 0)
        self.assertIn("亚洲（15 个国家）", out)
        self.assertIn("中国", out)
        self.assertIn("北京", out)

    def test_list_english_alias(self) -> None:
        code, out, _err = self.run_cli(["list", "asia"])
        self.assertEqual(code, 0)
        self.assertIn("15 个国家", out)

    def test_list_unknown(self) -> None:
        code, _out, err = self.run_cli(["list", "南极洲"])
        self.assertEqual(code, 2)
        self.assertIn("未知大洲", err)
        self.assertIn("大洋洲", err)

    def test_list_missing_argument(self) -> None:
        code, _out, err = self.run_cli(["list"])
        self.assertEqual(code, 2)
        self.assertIn("缺少大洲名称", err)


class QuizCliTests(CliTestCase):
    def test_quiz_writes_file(self) -> None:
        path = self.output_path("quiz.html")
        code, out, _err = self.run_cli(
            ["quiz", "--count", "10", "--seed", "5", "-o", path]
        )
        self.assertEqual(code, 0)
        self.assertIn("已生成：", out)
        self.assertTrue(os.path.isfile(path))
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertTrue(content.startswith("<!DOCTYPE html>"))
        self.assertEqual(content.count('class="question"'), 10)

    def test_quiz_default_count_is_ten(self) -> None:
        path = self.output_path("default.html")
        code, _out, _err = self.run_cli(["quiz", "-o", path])
        self.assertEqual(code, 0)
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertEqual(content.count('class="question"'), 10)

    def test_quiz_prints_to_stdout(self) -> None:
        code, out, _err = self.run_cli(["quiz", "--count", "2", "--seed", "1"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("<!DOCTYPE html>"))

    def test_quiz_seed_is_reproducible(self) -> None:
        first = self.output_path("first.html")
        second = self.output_path("second.html")
        self.run_cli(["quiz", "--count", "8", "--seed", "42", "-o", first])
        self.run_cli(["quiz", "--count", "8", "--seed", "42", "-o", second])
        with open(first, encoding="utf-8") as handle:
            content_a = handle.read()
        with open(second, encoding="utf-8") as handle:
            content_b = handle.read()
        self.assertEqual(content_a, content_b)

    def test_quiz_count_not_a_number(self) -> None:
        code, _out, err = self.run_cli(["quiz", "--count", "abc"])
        self.assertEqual(code, 2)
        self.assertIn("题目数量必须是整数", err)

    def test_quiz_count_zero(self) -> None:
        code, _out, err = self.run_cli(["quiz", "--count", "0"])
        self.assertEqual(code, 2)
        self.assertIn("1 到 40", err)

    def test_quiz_count_above_limit(self) -> None:
        code, _out, err = self.run_cli(["quiz", "--count", "41"])
        self.assertEqual(code, 2)
        self.assertIn("1 到 40", err)

    def test_quiz_continent(self) -> None:
        path = self.output_path("asia.html")
        code, _out, _err = self.run_cli(
            ["quiz", "--count", "5", "--seed", "3", "--continent", "亚洲", "-o", path]
        )
        self.assertEqual(code, 0)
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertEqual(content.count('class="question"'), 5)

    def test_quiz_continent_too_small(self) -> None:
        code, _out, err = self.run_cli(
            ["quiz", "--count", "10", "--continent", "大洋洲"]
        )
        self.assertEqual(code, 2)
        self.assertIn("大洋洲", err)

    def test_quiz_negative_seed(self) -> None:
        path = self.output_path("negative.html")
        code, _out, _err = self.run_cli(
            ["quiz", "--count", "3", "--seed", "-7", "-o", path]
        )
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(path))

    def test_quiz_unknown_option(self) -> None:
        code, _out, err = self.run_cli(["quiz", "--foo", "1"])
        self.assertEqual(code, 2)
        self.assertIn("未知选项", err)

    def test_quiz_missing_option_value(self) -> None:
        code, _out, err = self.run_cli(["quiz", "--count"])
        self.assertEqual(code, 2)
        self.assertIn("缺少取值", err)

    def test_quiz_extra_positional(self) -> None:
        code, _out, err = self.run_cli(["quiz", "5"])
        self.assertEqual(code, 2)
        self.assertIn("不接受额外参数", err)


class MatchCliTests(CliTestCase):
    def test_match_writes_file(self) -> None:
        path = self.output_path("match.html")
        code, out, _err = self.run_cli(
            ["match", "--count", "6", "--seed", "2", "-o", path]
        )
        self.assertEqual(code, 0)
        self.assertIn("已生成：", out)
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("配对", content)
        self.assertEqual(content.count('class="letter"'), 6)

    def test_match_bad_count(self) -> None:
        code, _out, err = self.run_cli(["match", "--count", "21"])
        self.assertEqual(code, 2)
        self.assertIn("1 到 20", err)

    def test_match_rejects_continent(self) -> None:
        code, _out, err = self.run_cli(["match", "--continent", "亚洲"])
        self.assertEqual(code, 2)
        self.assertIn("不支持 --continent", err)

    def test_match_prints_to_stdout(self) -> None:
        code, out, _err = self.run_cli(["match", "--count", "2", "--seed", "4"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("<!DOCTYPE html>"))


class TableCliTests(CliTestCase):
    def test_table_writes_file(self) -> None:
        path = self.output_path("table.html")
        code, out, _err = self.run_cli(["table", "-o", path])
        self.assertEqual(code, 0)
        self.assertIn("已生成：", out)
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("非洲", content)
        self.assertIn("大洋洲", content)

    def test_table_prints_to_stdout(self) -> None:
        code, out, _err = self.run_cli(["table"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("<!DOCTYPE html>"))
        self.assertIn("美洲", out)

    def test_table_rejects_count(self) -> None:
        code, _out, err = self.run_cli(["table", "--count", "5"])
        self.assertEqual(code, 2)
        self.assertIn("只支持", err)

    def test_table_creates_nested_directory(self) -> None:
        path = os.path.join(self.tmpdir, "nested", "deep", "table.html")
        code, _out, _err = self.run_cli(["table", "--output", path])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(path))

    def test_table_write_failure(self) -> None:
        code, _out, err = self.run_cli(["table", "-o", self.tmpdir])
        self.assertEqual(code, 2)
        self.assertIn("无法写入文件", err)


class ErrorHandlingTests(CliTestCase):
    def test_unknown_command(self) -> None:
        code, _out, err = self.run_cli(["bogus"])
        self.assertEqual(code, 2)
        self.assertIn("未知命令", err)

    def test_argv_must_be_sequence(self) -> None:
        code, _out, err = self.run_cli("capital 日本")  # type: ignore[arg-type]
        self.assertEqual(code, 2)
        self.assertIn("命令行参数", err)

    def test_argv_items_must_be_strings(self) -> None:
        code, _out, err = self.run_cli(["capital", 123])  # type: ignore[list-item]
        self.assertEqual(code, 2)
        self.assertIn("字符串", err)

    def test_main_reads_sys_argv(self) -> None:
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["worldcapitals", "capital", "日本"]):
            with contextlib.redirect_stdout(out):
                code = main()
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "东京")

    def test_ensure_utf8_console_returns_none(self) -> None:
        self.assertIsNone(_ensure_utf8_console())


if __name__ == "__main__":
    unittest.main()
