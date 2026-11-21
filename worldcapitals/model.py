"""世界国家与首都的数据模型。

本模块只依赖 Python 标准库，兼容 Python 3.9 及以上版本。
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

__all__ = [
    "CONTINENTS",
    "Country",
    "all_countries",
    "capital_of",
    "country_of",
    "list_by_continent",
    "match_items",
    "normalize",
    "quiz_items",
]

CONTINENTS: Tuple[str, ...] = (
    "亚洲",
    "欧洲",
    "非洲",
    "北美洲",
    "南美洲",
    "大洋洲",
)

_CONTINENT_ALIASES: Dict[str, str] = {
    "亚洲": "亚洲",
    "亚洲国家": "亚洲",
    "asia": "亚洲",
    "欧洲": "欧洲",
    "欧洲国家": "欧洲",
    "europe": "欧洲",
    "非洲": "非洲",
    "非洲国家": "非洲",
    "africa": "非洲",
    "北美洲": "北美洲",
    "北美洲国家": "北美洲",
    "北美": "北美洲",
    "north america": "北美洲",
    "northamerica": "北美洲",
    "南美洲": "南美洲",
    "南美洲国家": "南美洲",
    "南美": "南美洲",
    "south america": "南美洲",
    "southamerica": "南美洲",
    "大洋洲": "大洋洲",
    "大洋洲国家": "大洋洲",
    "oceania": "大洋洲",
}


@dataclass(frozen=True)
class Country:
    """一个国家及其首都的静态信息。"""

    country_zh: str
    country_en: str
    capital_zh: str
    capital_en: str
    continent: str
    aliases: Tuple[str, ...] = ()


_COUNTRIES: Tuple[Country, ...] = (
    # 亚洲（15）
    Country("中国", "China", "北京", "Beijing", "亚洲", ("中华人民共和国", "PRC")),
    Country("日本", "Japan", "东京", "Tokyo", "亚洲", ("日本国", "Nippon")),
    Country(
        "韩国",
        "South Korea",
        "首尔",
        "Seoul",
        "亚洲",
        ("大韩民国", "Korea", "Republic of Korea", "南韩"),
    ),
    Country("印度", "India", "新德里", "New Delhi", "亚洲", ("印度共和国",)),
    Country("印度尼西亚", "Indonesia", "雅加达", "Jakarta", "亚洲", ("印尼",)),
    Country("菲律宾", "Philippines", "马尼拉", "Manila", "亚洲", ("菲律宾共和国",)),
    Country("泰国", "Thailand", "曼谷", "Bangkok", "亚洲", ("泰王国",)),
    Country(
        "越南",
        "Vietnam",
        "河内",
        "Hanoi",
        "亚洲",
        ("越南社会主义共和国", "Viet Nam"),
    ),
    Country("马来西亚", "Malaysia", "吉隆坡", "Kuala Lumpur", "亚洲", ("大马",)),
    Country("新加坡", "Singapore", "新加坡", "Singapore", "亚洲", ("狮城",)),
    Country("巴基斯坦", "Pakistan", "伊斯兰堡", "Islamabad", "亚洲", ()),
    Country("伊朗", "Iran", "德黑兰", "Tehran", "亚洲", ("伊朗伊斯兰共和国",)),
    Country("沙特阿拉伯", "Saudi Arabia", "利雅得", "Riyadh", "亚洲", ("沙特",)),
    Country(
        "土耳其",
        "Turkey",
        "安卡拉",
        "Ankara",
        "亚洲",
        ("土耳其共和国", "Turkiye"),
    ),
    Country("蒙古", "Mongolia", "乌兰巴托", "Ulaanbaatar", "亚洲", ("蒙古国",)),
    # 欧洲（15）
    Country(
        "英国",
        "United Kingdom",
        "伦敦",
        "London",
        "欧洲",
        ("UK", "Britain", "Great Britain", "大不列颠"),
    ),
    Country("法国", "France", "巴黎", "Paris", "欧洲", ("法兰西",)),
    Country("德国", "Germany", "柏林", "Berlin", "欧洲", ("德意志",)),
    Country("意大利", "Italy", "罗马", "Rome", "欧洲", ("义大利",)),
    Country("西班牙", "Spain", "马德里", "Madrid", "欧洲", ()),
    Country("葡萄牙", "Portugal", "里斯本", "Lisbon", "欧洲", ()),
    Country("荷兰", "Netherlands", "阿姆斯特丹", "Amsterdam", "欧洲", ("Holland", "尼德兰")),
    Country("比利时", "Belgium", "布鲁塞尔", "Brussels", "欧洲", ()),
    Country("瑞士", "Switzerland", "伯尔尼", "Bern", "欧洲", ("瑞士联邦",)),
    Country("奥地利", "Austria", "维也纳", "Vienna", "欧洲", ()),
    Country("瑞典", "Sweden", "斯德哥尔摩", "Stockholm", "欧洲", ()),
    Country("挪威", "Norway", "奥斯陆", "Oslo", "欧洲", ()),
    Country("丹麦", "Denmark", "哥本哈根", "Copenhagen", "欧洲", ()),
    Country("芬兰", "Finland", "赫尔辛基", "Helsinki", "欧洲", ()),
    Country("波兰", "Poland", "华沙", "Warsaw", "欧洲", ()),
    # 非洲（12）
    Country("埃及", "Egypt", "开罗", "Cairo", "非洲", ()),
    Country("肯尼亚", "Kenya", "内罗毕", "Nairobi", "非洲", ()),
    Country("尼日利亚", "Nigeria", "阿布贾", "Abuja", "非洲", ()),
    Country("埃塞俄比亚", "Ethiopia", "亚的斯亚贝巴", "Addis Ababa", "非洲", ()),
    Country("摩洛哥", "Morocco", "拉巴特", "Rabat", "非洲", ()),
    Country("阿尔及利亚", "Algeria", "阿尔及尔", "Algiers", "非洲", ()),
    Country("突尼斯", "Tunisia", "突尼斯", "Tunis", "非洲", ()),
    Country("加纳", "Ghana", "阿克拉", "Accra", "非洲", ()),
    Country("坦桑尼亚", "Tanzania", "多多马", "Dodoma", "非洲", ()),
    Country("乌干达", "Uganda", "坎帕拉", "Kampala", "非洲", ()),
    Country("赞比亚", "Zambia", "卢萨卡", "Lusaka", "非洲", ()),
    Country("塞内加尔", "Senegal", "达喀尔", "Dakar", "非洲", ()),
    # 北美洲（10）
    Country(
        "美国",
        "United States",
        "华盛顿",
        "Washington, D.C.",
        "北美洲",
        ("US", "USA", "America", "美利坚合众国"),
    ),
    Country("加拿大", "Canada", "渥太华", "Ottawa", "北美洲", ()),
    Country("墨西哥", "Mexico", "墨西哥城", "Mexico City", "北美洲", ()),
    Country("古巴", "Cuba", "哈瓦那", "Havana", "北美洲", ()),
    Country("牙买加", "Jamaica", "金斯敦", "Kingston", "北美洲", ()),
    Country("巴拿马", "Panama", "巴拿马城", "Panama City", "北美洲", ()),
    Country("哥斯达黎加", "Costa Rica", "圣何塞", "San Jose", "北美洲", ()),
    Country("危地马拉", "Guatemala", "危地马拉城", "Guatemala City", "北美洲", ()),
    Country(
        "多米尼加",
        "Dominican Republic",
        "圣多明各",
        "Santo Domingo",
        "北美洲",
        ("多米尼加共和国",),
    ),
    Country("洪都拉斯", "Honduras", "特古西加尔巴", "Tegucigalpa", "北美洲", ()),
    # 南美洲（8）
    Country("巴西", "Brazil", "巴西利亚", "Brasilia", "南美洲", ("Brasil",)),
    Country("阿根廷", "Argentina", "布宜诺斯艾利斯", "Buenos Aires", "南美洲", ()),
    Country("智利", "Chile", "圣地亚哥", "Santiago", "南美洲", ()),
    Country("秘鲁", "Peru", "利马", "Lima", "南美洲", ()),
    Country("哥伦比亚", "Colombia", "波哥大", "Bogota", "南美洲", ()),
    Country("委内瑞拉", "Venezuela", "加拉加斯", "Caracas", "南美洲", ()),
    Country("乌拉圭", "Uruguay", "蒙得维的亚", "Montevideo", "南美洲", ()),
    Country("厄瓜多尔", "Ecuador", "基多", "Quito", "南美洲", ()),
    # 大洋洲（5）
    Country("澳大利亚", "Australia", "堪培拉", "Canberra", "大洋洲", ("澳洲",)),
    Country("新西兰", "New Zealand", "惠灵顿", "Wellington", "大洋洲", ()),
    Country("斐济", "Fiji", "苏瓦", "Suva", "大洋洲", ()),
    Country(
        "巴布亚新几内亚",
        "Papua New Guinea",
        "莫尔兹比港",
        "Port Moresby",
        "大洋洲",
        ("巴新",),
    ),
    Country("萨摩亚", "Samoa", "阿皮亚", "Apia", "大洋洲", ()),
)


def normalize(text: str) -> str:
    """去除首尾空白、压缩内部空白，并把英文统一为小写。"""
    if not isinstance(text, str):
        raise TypeError("待处理的文本必须是字符串")
    return " ".join(text.split()).casefold()


def _build_country_index() -> Dict[str, Country]:
    index: Dict[str, Country] = {}
    for country in _COUNTRIES:
        names = (country.country_zh, country.country_en) + country.aliases
        for name in names:
            index.setdefault(normalize(name), country)
    return index


def _build_capital_index() -> Dict[str, Country]:
    index: Dict[str, Country] = {}
    for country in _COUNTRIES:
        index.setdefault(normalize(country.capital_zh), country)
        index.setdefault(normalize(country.capital_en), country)
    return index


_COUNTRY_INDEX: Dict[str, Country] = _build_country_index()
_CAPITAL_INDEX: Dict[str, Country] = _build_capital_index()


def all_countries() -> List[Country]:
    """返回全部国家（按大洲顺序排列的副本）。"""
    return list(_COUNTRIES)


def capital_of(query: str) -> str:
    """按中文国名、英文国名或别名查询中文首都名称。"""
    if not isinstance(query, str):
        raise TypeError("国家名称必须是字符串")
    key = normalize(query)
    if not key:
        raise ValueError("国家名称不能为空（当前收录 %d 个国家）" % len(_COUNTRIES))
    country = _COUNTRY_INDEX.get(key)
    if country is None:
        raise ValueError(
            "未知国家：%s（当前收录 %d 个国家）" % (" ".join(query.split()), len(_COUNTRIES))
        )
    return country.capital_zh


def country_of(query: str) -> str:
    """按中文首都名或英文首都名反查中文国名。"""
    if not isinstance(query, str):
        raise TypeError("首都名称必须是字符串")
    key = normalize(query)
    if not key:
        raise ValueError("首都名称不能为空（当前收录 %d 个首都）" % len(_COUNTRIES))
    country = _CAPITAL_INDEX.get(key)
    if country is None:
        raise ValueError(
            "未知首都：%s（当前收录 %d 个首都）" % (" ".join(query.split()), len(_COUNTRIES))
        )
    return country.country_zh


def _resolve_continent(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("大洲名称必须是字符串")
    key = normalize(value)
    if not key:
        raise ValueError("大洲名称不能为空（可选：%s）" % "、".join(CONTINENTS))
    name = _CONTINENT_ALIASES.get(key)
    if name is None:
        raise ValueError(
            "未知大洲：%s（可选：%s）" % (" ".join(value.split()), "、".join(CONTINENTS))
        )
    return name


def list_by_continent(continent: str) -> List[Country]:
    """按大洲筛选国家，支持「亚洲」「亚洲国家」「asia」等写法。"""
    name = _resolve_continent(continent)
    return [country for country in _COUNTRIES if country.continent == name]


def _validate_count(value: object, label: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s必须是整数" % label)
    if value < minimum or value > maximum:
        raise ValueError("%s必须在 %d 到 %d 之间" % (label, minimum, maximum))
    return value


def _validate_seed(value: Optional[int]) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("随机种子必须是整数或 None")
    return value


def quiz_items(
    count: int,
    seed: Optional[int] = None,
    continent: Optional[str] = None,
) -> List[Dict[str, object]]:
    """生成四选一的选择题，干扰项优先来自同一大洲。"""
    _validate_count(count, "题目数量", 1, 40)
    _validate_seed(seed)

    if continent is None:
        pool: List[Country] = list(_COUNTRIES)
        scope = "全球"
    else:
        pool = list_by_continent(continent)
        scope = pool[0].continent if pool else "该大洲"

    if count > len(pool):
        raise ValueError(
            "%s仅有 %d 个国家，无法生成 %d 道题" % (scope, len(pool), count)
        )

    rng = random.Random(seed)
    selected = rng.sample(pool, count)
    items: List[Dict[str, object]] = []

    for country in selected:
        same_continent = [
            other.capital_zh
            for other in pool
            if other.continent == country.continent
            and other.capital_zh != country.capital_zh
        ]
        other_continent = [
            other.capital_zh
            for other in _COUNTRIES
            if other.continent != country.continent
            and other.capital_zh != country.capital_zh
        ]
        rng.shuffle(same_continent)
        rng.shuffle(other_continent)

        distractors: List[str] = []
        for candidate in same_continent + other_continent:
            if candidate not in distractors:
                distractors.append(candidate)
            if len(distractors) == 3:
                break

        if len(distractors) < 3:
            raise ValueError("可用首都数量不足，无法为 %s 生成四个选项" % country.country_zh)

        options = [country.capital_zh] + distractors
        rng.shuffle(options)

        items.append(
            {
                "country_zh": country.country_zh,
                "country_en": country.country_en,
                "continent": country.continent,
                "question": "%s的首都是？" % country.country_zh,
                "options": options,
                "answer": country.capital_zh,
            }
        )

    return items


def match_items(count: int, seed: Optional[int] = None) -> List[Tuple[str, str]]:
    """生成国家与首都的配对练习。"""
    _validate_count(count, "配对数量", 1, 20)
    _validate_seed(seed)

    rng = random.Random(seed)
    selected = rng.sample(list(_COUNTRIES), count)
    return [(country.country_zh, country.capital_zh) for country in selected]
