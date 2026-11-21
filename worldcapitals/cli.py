"""worldcapitals 命令行入口。"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional, Sequence, Tuple

from . import render
from .model import (
    all_countries,
    capital_of,
    country_of,
    list_by_continent,
    match_items,
    quiz_items,
)

__all__ = ["main"]

_USAGE = """用法：
  worldcapitals capital <国家>          查询某国首都
  worldcapitals country <首都>          查询首都在哪个国家
  worldcapitals list <大洲>             按大洲列出国家与首都
  worldcapitals quiz [选项]             生成四选一练习页
  worldcapitals match [选项]            生成国家—首都配对页
  worldcapitals table [选项]            生成按大洲分组的总表

选项：
  quiz:  --count N（1-40，默认 10）  --seed S  --continent 大洲  -o 文件
  match: --count N（1-20，默认 10）  --seed S  -o 文件
  table: -o 文件
  通用:  -h, --help                     显示本帮助
"""

_OPTION_SPECS: Dict[str, str] = {
    "--count": "count",
    "--seed": "seed",
    "--continent": "continent",
    "-o": "output",
    "--output": "output",
}


def _ensure_utf8_console() -> None:
    """尽量把标准输出与标准错误切换为 UTF-8，失败时保持原样。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            continue


def _parse_options(
    args: Sequence[str], allowed: Dict[str, str]
) -> Tuple[Dict[str, str], List[str]]:
    values: Dict[str, str] = {}
    positionals: List[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        if token.startswith("-") and token != "-":
            key = allowed.get(token)
            if key is None:
                raise ValueError("未知选项：%s" % token)
            if index + 1 >= len(args):
                raise ValueError("选项 %s 缺少取值" % token)
            values[key] = args[index + 1]
            index += 2
        else:
            positionals.append(token)
            index += 1
    return values, positionals


def _parse_int(raw: str, label: str, minimum: int, maximum: int) -> int:
    try:
        number = int(raw)
    except ValueError:
        raise ValueError("%s必须是整数：%s" % (label, raw)) from None
    if number < minimum or number > maximum:
        raise ValueError("%s必须在 %d 到 %d 之间" % (label, minimum, maximum))
    return number


def _parse_optional_int(raw: Optional[str], label: str) -> Optional[int]:
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        raise ValueError("%s必须是整数：%s" % (label, raw)) from None


def _write_file(path: str, content: str) -> None:
    if not isinstance(path, str) or not path.strip():
        raise ValueError("输出路径不能为空")
    try:
        directory = os.path.dirname(os.path.abspath(path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
    except OSError as exc:
        raise ValueError("无法写入文件 %s：%s" % (path, exc)) from exc
    print("已生成：%s" % path)


def _emit(content: str, path: Optional[str]) -> int:
    if path is None:
        print(content, end="")
    else:
        _write_file(path, content)
    return 0


def _join_query(args: Sequence[str], label: str, command: str) -> str:
    if not args:
        raise ValueError("缺少%s，用法：worldcapitals %s <%s>" % (label, command, label))
    return " ".join(args)


def _run_capital(args: Sequence[str]) -> int:
    query = _join_query(args, "国家名称", "capital")
    print(capital_of(query))
    return 0


def _run_country(args: Sequence[str]) -> int:
    query = _join_query(args, "首都名称", "country")
    print(country_of(query))
    return 0


def _run_list(args: Sequence[str]) -> int:
    continent = _join_query(args, "大洲名称", "list")
    countries = list_by_continent(continent)
    if not countries:
        raise ValueError("该大洲暂无国家数据")
    print("%s（%d 个国家）" % (countries[0].continent, len(countries)))
    for index, country in enumerate(countries, 1):
        print(
            "%d. %s / %s — %s / %s"
            % (
                index,
                country.country_zh,
                country.country_en,
                country.capital_zh,
                country.capital_en,
            )
        )
    return 0


def _run_quiz(args: Sequence[str]) -> int:
    values, positionals = _parse_options(args, _OPTION_SPECS)
    if positionals:
        raise ValueError("quiz 不接受额外参数：%s" % " ".join(positionals))

    count = _parse_int(values.get("count", "10"), "题目数量", 1, 40)
    seed = _parse_optional_int(values.get("seed"), "随机种子")
    items = quiz_items(count, seed, values.get("continent"))
    document = render.quiz_html(items, "世界首都练习题")
    return _emit(document, values.get("output"))


def _run_match(args: Sequence[str]) -> int:
    values, positionals = _parse_options(args, _OPTION_SPECS)
    if positionals:
        raise ValueError("match 不接受额外参数：%s" % " ".join(positionals))
    if "continent" in values:
        raise ValueError("match 不支持 --continent 选项")

    count = _parse_int(values.get("count", "10"), "配对数量", 1, 20)
    seed = _parse_optional_int(values.get("seed"), "随机种子")
    pairs = match_items(count, seed)
    document = render.match_html(pairs, "国家与首都配对练习")
    return _emit(document, values.get("output"))


def _run_table(args: Sequence[str]) -> int:
    values, positionals = _parse_options(args, _OPTION_SPECS)
    if positionals:
        raise ValueError("table 不接受额外参数：%s" % " ".join(positionals))
    if "count" in values or "seed" in values or "continent" in values:
        raise ValueError("table 只支持 -o/--output 选项")

    document = render.table_html(all_countries(), "世界国家与首都总表")
    return _emit(document, values.get("output"))


def _run(args: Sequence[str]) -> int:
    if not args or args[0] in ("-h", "--help", "help"):
        print(_USAGE, end="")
        return 0

    command = args[0]
    rest = list(args[1:])
    if command == "capital":
        return _run_capital(rest)
    if command == "country":
        return _run_country(rest)
    if command == "list":
        return _run_list(rest)
    if command == "quiz":
        return _run_quiz(rest)
    if command == "match":
        return _run_match(rest)
    if command == "table":
        return _run_table(rest)
    raise ValueError(
        "未知命令：%s（可用：capital、country、list、quiz、match、table）" % command
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """执行命令行；成功返回 0，参数错误返回 2。"""
    _ensure_utf8_console()
    try:
        if argv is None:
            args = list(sys.argv[1:])
        else:
            if isinstance(argv, (str, bytes)) or not isinstance(argv, (list, tuple)):
                raise TypeError("命令行参数必须是字符串序列")
            args = list(argv)
        if any(not isinstance(item, str) for item in args):
            raise TypeError("命令行参数必须全部是字符串")
        return _run(args)
    except (TypeError, ValueError) as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2
