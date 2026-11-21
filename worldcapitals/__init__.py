"""世界国家与首都：中英查询、大洲分组与可打印练习页。"""

from __future__ import annotations

from .model import (
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
from .render import match_html, quiz_html, table_html
from .cli import main

__version__ = "0.1.0"

__all__ = [
    "CONTINENTS",
    "Country",
    "__version__",
    "all_countries",
    "capital_of",
    "country_of",
    "list_by_continent",
    "main",
    "match_html",
    "match_items",
    "normalize",
    "quiz_html",
    "quiz_items",
    "table_html",
]
