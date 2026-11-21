"""把国家、首都数据渲染为可打印的 HTML 页面。"""

from __future__ import annotations

import html
from typing import Dict, List, Sequence, Tuple

from .model import CONTINENTS, Country

__all__ = ["match_html", "quiz_html", "table_html"]

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

_STYLE = """
:root {
  --ink: #1f2933;
  --muted: #52606d;
  --line: #cbd2d9;
  --accent: #0b5f8a;
  --paper: #ffffff;
  --tint: #f5f7fa;
}
* { box-sizing: border-box; }
html { font-size: 11pt; }
body {
  margin: 0;
  padding: 18px;
  color: var(--ink);
  background: var(--tint);
  font-family: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "Source Han Sans SC", sans-serif;
  line-height: 1.55;
}
.sheet {
  max-width: 190mm;
  margin: 0 auto;
  padding: 14mm;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 6px;
}
header { margin-bottom: 8mm; border-bottom: 2px solid var(--accent); padding-bottom: 4mm; }
h1 { margin: 0 0 2mm; font-size: 20pt; letter-spacing: 1px; }
h2 { margin: 6mm 0 2mm; font-size: 13pt; color: var(--accent); }
p { margin: 1mm 0; }
.hint { color: var(--muted); font-size: 9.5pt; }
.empty { padding: 8mm; text-align: center; color: var(--muted); }
.quiz { display: block; }
.question {
  padding: 3mm 0;
  border-bottom: 1px dashed var(--line);
  break-inside: avoid;
  page-break-inside: avoid;
}
.question:last-child { border-bottom: none; }
.q { font-weight: 600; margin-bottom: 2mm; }
.no { display: inline-block; min-width: 8mm; color: var(--accent); }
.options { list-style: none; margin: 0; padding: 0 0 0 8mm; }
.options li { padding: 1mm 0; }
.letter {
  display: inline-block;
  width: 6mm;
  height: 6mm;
  margin-right: 2mm;
  border: 1px solid var(--line);
  border-radius: 50%;
  text-align: center;
  line-height: 6mm;
  font-size: 8.5pt;
  color: var(--accent);
}
.answers { margin-top: 6mm; padding-top: 4mm; border-top: 2px solid var(--accent); }
.answers ol { margin: 0; padding-left: 8mm; }
.match-grid { display: flex; gap: 8mm; align-items: flex-start; }
.match-grid > div { flex: 1 1 0; min-width: 0; }
.match-grid ol { margin: 0; padding-left: 0; list-style: none; }
.match-grid li {
  padding: 1.6mm 0;
  border-bottom: 1px dotted var(--line);
  break-inside: avoid;
}
table { width: 100%; border-collapse: collapse; font-size: 10pt; }
th, td { border: 1px solid var(--line); padding: 1.6mm 2mm; text-align: left; }
th { background: var(--tint); font-weight: 600; }
tbody tr:nth-child(even) { background: #fbfcfd; }
@page { size: A4; margin: 14mm; }
@media print {
  body { background: #ffffff; padding: 0; font-size: 10.5pt; }
  .sheet { max-width: none; margin: 0; padding: 0; border: none; border-radius: 0; }
  .no-print { display: none !important; }
  h1 { font-size: 18pt; }
  table { page-break-inside: auto; }
  tr, .question, .match-grid li { break-inside: avoid; page-break-inside: avoid; }
}
"""


def _text(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError("%s必须是字符串" % label)
    return html.escape(value, quote=True)


def _as_list(values: object, label: str) -> List[object]:
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise TypeError("%s必须是列表或元组" % label)
    return list(values)


def _document(title: str, subtitle: str, body: str) -> str:
    safe_title = _text(title, "标题")
    safe_subtitle = _text(subtitle, "副标题")
    return (
        "<!DOCTYPE html>\n"
        '<html lang="zh-CN">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>%s</title>\n"
        "<style>%s</style>\n"
        "</head>\n"
        "<body>\n"
        '<main class="sheet">\n'
        "<header>\n"
        "<h1>%s</h1>\n"
        '<p class="hint">%s</p>\n'
        "</header>\n"
        "%s\n"
        "</main>\n"
        "</body>\n"
        "</html>\n"
    ) % (safe_title, _STYLE, safe_title, safe_subtitle, body)


def _quiz_item_html(item: object, index: int) -> Tuple[str, str]:
    if not isinstance(item, dict):
        raise TypeError("第 %d 道题必须是字典" % index)

    for key in ("question", "options", "answer"):
        if key not in item:
            raise ValueError("第 %d 道题缺少字段：%s" % (index, key))

    question = _text(item["question"], "题干")
    raw_options = _as_list(item["options"], "选项")
    options = [_text(option, "选项") for option in raw_options]
    if len(options) < 2:
        raise ValueError("第 %d 道题至少需要 2 个选项" % index)
    if len(set(options)) != len(options):
        raise ValueError("第 %d 道题存在重复选项" % index)

    answer = _text(item["answer"], "答案")
    if answer not in options:
        raise ValueError("第 %d 道题的答案不在选项中" % index)

    option_lines: List[str] = []
    for position, option in enumerate(options):
        if position < len(_LETTERS):
            letter = _LETTERS[position]
        else:
            letter = str(position + 1)
        option_lines.append(
            '<li><span class="letter">%s</span>%s</li>' % (letter, option)
        )

    block = (
        '<section class="question">\n'
        '<p class="q"><span class="no">%d.</span>%s</p>\n'
        '<ol class="options">\n%s\n</ol>\n'
        "</section>"
    ) % (index, question, "\n".join(option_lines))
    return block, answer


def quiz_html(
    items: Sequence[Dict[str, object]],
    title: str = "世界首都练习",
    with_answers: bool = False,
) -> str:
    """渲染选择题页面；with_answers 为真时附加参考答案。"""
    if not isinstance(with_answers, bool):
        raise TypeError("with_answers 必须是布尔值")

    raw_items = _as_list(items, "题目列表")
    blocks: List[str] = []
    answers: List[str] = []
    for index, item in enumerate(raw_items, 1):
        block, answer = _quiz_item_html(item, index)
        blocks.append(block)
        answers.append(answer)

    if blocks:
        body = '<div class="quiz">\n%s\n</div>' % "\n".join(blocks)
    else:
        body = '<p class="empty">暂无题目</p>'

    if with_answers:
        answer_lines: List[str] = []
        for index, answer in enumerate(answers, 1):
            answer_lines.append("<li>%d. %s</li>" % (index, answer))
        body += (
            '\n<section class="answers">\n<h2>参考答案</h2>\n<ol>\n%s\n</ol>\n</section>'
            % "\n".join(answer_lines)
        )

    subtitle = "共 %d 题 · 每题只有一个正确答案" % len(blocks)
    return _document(title, subtitle, body)


def match_html(
    pairs: Sequence[Tuple[str, str]],
    title: str = "国家与首都配对",
) -> str:
    """渲染国家—首都配对页面，右侧首都按逆序排列以便连线。"""
    raw_pairs = _as_list(pairs, "配对列表")
    validated: List[Tuple[str, str]] = []
    for index, pair in enumerate(raw_pairs, 1):
        if isinstance(pair, (str, bytes)) or not isinstance(pair, (list, tuple)):
            raise TypeError("第 %d 组配对必须是二元组" % index)
        if len(pair) != 2:
            raise ValueError("第 %d 组配对必须包含国家和首都两个元素" % index)
        country = _text(pair[0], "配对中的国家")
        capital = _text(pair[1], "配对中的首都")
        validated.append((country, capital))

    if not validated:
        body = '<p class="empty">暂无配对题目</p>'
    else:
        country_lines: List[str] = []
        capital_lines: List[str] = []
        for index, (country, _capital) in enumerate(validated, 1):
            country_lines.append('<li><span class="no">%d.</span>%s</li>' % (index, country))
        reversed_pairs = list(reversed(validated))
        for index, (_country, capital) in enumerate(reversed_pairs):
            letter = _LETTERS[index] if index < len(_LETTERS) else str(index + 1)
            capital_lines.append(
                '<li><span class="letter">%s</span>%s</li>' % (letter, capital)
            )
        body = (
            '<p class="hint">把右侧首都的字母写在左侧国家后的括号内。</p>\n'
            '<div class="match-grid">\n'
            "<div>\n<h2>国家</h2>\n<ol>\n%s\n</ol>\n</div>\n"
            "<div>\n<h2>首都</h2>\n<ol>\n%s\n</ol>\n</div>\n"
            "</div>"
        ) % ("\n".join(country_lines), "\n".join(capital_lines))

    subtitle = "共 %d 组 · 一一对应" % len(validated)
    return _document(title, subtitle, body)


def table_html(
    countries: Sequence[Country],
    title: str = "世界国家与首都总表",
) -> str:
    """按大洲分组渲染总表。"""
    raw_countries = _as_list(countries, "国家列表")
    grouped: Dict[str, List[Country]] = {}
    for item in raw_countries:
        if not isinstance(item, Country):
            raise TypeError("国家列表只能包含 Country 对象")
        grouped.setdefault(item.continent, []).append(item)

    ordered: List[str] = [name for name in CONTINENTS if name in grouped]
    ordered.extend(name for name in grouped if name not in CONTINENTS)

    sections: List[str] = []
    for continent in ordered:
        rows: List[str] = []
        for index, country in enumerate(grouped[continent], 1):
            rows.append(
                "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                % (
                    index,
                    _text(country.country_zh, "国家中文名"),
                    _text(country.country_en, "国家英文名"),
                    _text(country.capital_zh, "首都中文名"),
                    _text(country.capital_en, "首都英文名"),
                )
            )
        sections.append(
            "<section>\n<h2>%s（%d）</h2>\n"
            '<table>\n<thead>\n<tr><th>序号</th><th>国家</th><th>Country</th>'
            "<th>首都</th><th>Capital</th></tr>\n</thead>\n<tbody>\n%s\n</tbody>\n"
            "</table>\n</section>"
            % (_text(continent, "大洲名称"), len(grouped[continent]), "\n".join(rows))
        )

    if sections:
        body = "\n".join(sections)
    else:
        body = '<p class="empty">暂无国家数据</p>'

    subtitle = "共 %d 个国家 · 按大洲分组" % len(raw_countries)
    return _document(title, subtitle, body)
