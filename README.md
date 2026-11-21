# worldcapitals

[![CI](https://github.com/eastyou/worldcapitals/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/worldcapitals/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

世界国家与首都的轻量工具：支持中英文查询、按大洲分组，以及生成可直接打印的
A4 练习页（选择题、配对题、总表）。面向课堂与自学场景，零第三方依赖，只使用
Python 标准库。

## 特性

- 收录 **65 个国家**，覆盖亚洲（15）、欧洲（15）、非洲（12）、北美洲（10）、
  南美洲（8）、大洋洲（5）。
- 中文国名、英文国名、常见简称/旧译均可查询，例如 `美国`、`USA`、`UK`、`沙特`。
- 支持用中文或英文首都名反查国家。
- 大洲名称支持 `亚洲`、`亚洲国家`、`asia` 等多种写法。
- 生成四选一题目时优先使用同大洲国家作为干扰项，保证四个选项互不重复。
- 输出 HTML 自带 `@media print` 与 A4 页面设置，浏览器打开后可直接打印或存为 PDF。
- 所有公开函数均有类型注解，参数错误抛中文 `TypeError` / `ValueError`。
- **154 个单元测试**，已在 Python 3.9.6 与 Python 3.15.2 上全部通过。

## 安装

```bash
git clone https://github.com/eastyou/worldcapitals.git
cd worldcapitals
python3 -m pip install -e .
```

安装后会得到 `worldcapitals` 命令。也可以不安装，直接在项目根目录运行：

```bash
python3 -m worldcapitals --help
```

要求 Python **3.9+**，无第三方运行时依赖。

## 命令行用法

```bash
# 查询首都（支持英文与别名）
worldcapitals capital 日本
# 东京

worldcapitals capital USA
# 华盛顿

# 由首都反查国家
worldcapitals country 东京
# 日本

# 按大洲列出国家与首都
worldcapitals list 亚洲
# 亚洲（15 个国家）
# 1. 中国 / China — 北京 / Beijing
# 2. 日本 / Japan — 东京 / Tokyo
# ...

# 生成 10 道四选一练习题（同一种子结果可复现）
worldcapitals quiz --count 10 --seed 5 -o examples/quiz.html
# 已生成：examples/quiz.html

# 只出亚洲的题目
worldcapitals quiz --count 8 --seed 1 --continent 亚洲 -o examples/quiz-asia.html

# 生成国家—首都配对页
worldcapitals match --count 8 --seed 3 -o examples/match.html

# 生成按大洲分组的总表
worldcapitals table -o examples/capitals.html
```

不传 `-o` 时，HTML 会直接输出到标准输出，便于重定向：

```bash
worldcapitals table > capitals.html
```

### 选项说明

| 命令 | 选项 | 说明 |
| --- | --- | --- |
| `quiz` | `--count N` | 题目数量，1–40，默认 10 |
| `quiz` | `--seed S` | 随机种子，整数，相同种子结果一致 |
| `quiz` | `--continent 大洲` | 只从指定大洲出题 |
| `quiz` | `-o 文件` | 写入 HTML 文件，终端打印 `已生成：<路径>` |
| `match` | `--count N` | 配对数量，1–20，默认 10 |
| `match` | `--seed S` | 随机种子 |
| `match` | `-o 文件` | 写入 HTML 文件 |
| `table` | `-o 文件` | 写入 HTML 文件 |

参数错误时，程序把中文错误信息写入标准错误并返回退出码 `2`：

```text
$ worldcapitals capital 火星
错误：未知国家：火星（当前收录 65 个国家）
$ echo $?
2
```

## 库用法

```python
from worldcapitals import (
    all_countries,
    capital_of,
    country_of,
    list_by_continent,
    quiz_items,
    quiz_html,
)

print(len(all_countries()))        # 65
print(capital_of("日本"))           # 东京
print(capital_of("South Korea"))   # 首尔
print(country_of("Tokyo"))         # 日本

asia = list_by_continent("亚洲")
print(len(asia), asia[0].capital_zh)  # 15 北京

items = quiz_items(5, seed=2026, continent="亚洲")
document = quiz_html(items, "亚洲首都小测", with_answers=True)
with open("quiz.html", "w", encoding="utf-8") as handle:
    handle.write(document)
```

渲染函数均返回完整的 HTML 文档字符串：

- `quiz_html(items, title, with_answers=False)`：选择题，可附参考答案。
- `match_html(pairs, title)`：国家—首都配对，右侧首都逆序排列便于连线。
- `table_html(countries, title)`：按大洲分组的总表。

所有来自数据的文本都会经过 `html.escape`，可以安全展示用户输入或自定义标题。

## 示例文件

仓库内已生成以下可直接打开的示例：

- [`examples/capitals.html`](examples/capitals.html)：65 国按大洲分组的总表。
- [`examples/quiz.html`](examples/quiz.html)：10 道四选一练习题（种子 5）。
- [`examples/match.html`](examples/match.html)：8 组国家—首都配对页。

在浏览器中打开后按 `Ctrl/Cmd + P` 即可打印为 A4 或导出 PDF。

## 数据范围

| 大洲 | 国家数 | 示例 |
| --- | ---: | --- |
| 亚洲 | 15 | 中国—北京、日本—东京、印度—新德里 |
| 欧洲 | 15 | 英国—伦敦、法国—巴黎、德国—柏林 |
| 非洲 | 12 | 埃及—开罗、肯尼亚—内罗毕、摩洛哥—拉巴特 |
| 北美洲 | 10 | 美国—华盛顿、加拿大—渥太华、墨西哥—墨西哥城 |
| 南美洲 | 8 | 巴西—巴西利亚、阿根廷—布宜诺斯艾利斯 |
| 大洋洲 | 5 | 澳大利亚—堪培拉、新西兰—惠灵顿 |
| **合计** | **65** | |

每个国家包含：中文国名、英文国名、中文首都、英文首都、所属大洲、别名元组。
数据以 `Country` 冻结数据类保存，避免运行时被意外修改。

## 项目结构

```text
worldcapitals/
├── worldcapitals/
│   ├── __init__.py        # 公共 API 与 __version__
│   ├── __main__.py        # python -m worldcapitals
│   ├── model.py           # Country 数据、查询、出题
│   ├── render.py          # HTML 渲染
│   └── cli.py             # 命令行入口
├── tests/
│   ├── __init__.py
│   ├── test_model.py
│   ├── test_render.py
│   └── test_cli.py
├── examples/
│   ├── capitals.html
│   ├── quiz.html
│   └── match.html
├── .github/workflows/ci.yml
├── pyproject.toml
├── LICENSE
└── README.md
```

## 开发与测试

```bash
python3 -m unittest discover -s tests -v
```

当前共有 **154 个测试**，覆盖：

- 数据规模、大洲分布、字段完整性、只读性与名称唯一性；
- 中英文与别名查询、空输入、未知输入、类型错误；
- 大洲别名解析与六大洲兜底提示；
- 出题数量边界（1/40、1/20）、随机种子复现、选项唯一性与答案正确性；
- HTML 转义、空列表、缺字段、答案不在选项中等异常路径；
- CLI 全部子命令、文件输出、非法选项、退出码与标准错误。

两个解释器的真实执行结果：

```text
Python 3.9.6   Ran 154 tests ... OK
Python 3.15.2  Ran 154 tests ... OK
```

CI 在 Ubuntu / Windows / macOS 上运行 Python 3.10 与 3.13，并额外使用
ubuntu-22.04 + Python 3.9 验证向下兼容性。

## 兼容性说明

- 仅使用 Python 3.9+ 标准库：`dataclasses`、`random`、`html`、`os`、`sys` 等，
  命令行解析为轻量自研实现，不引入第三方依赖。
- 不使用 `X | None` 联合类型、`match` 语句、海象运算符等 3.10+ 语法。
- 所有模块均包含 `from __future__ import annotations`，类型注解使用
  `typing.Optional/List/Dict/Tuple/Sequence`。
- 文件读写统一使用 `encoding="utf-8"`，写入失败会把 `OSError` 转换为中文错误。

## 许可证

MIT © 2026 eastyou
