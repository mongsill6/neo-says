"""Quote database and selection logic."""

import json
import hashlib
import random
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Tuple


SUPPORTED_LANGS = ["en", "ko", "ja"]

_LANG_FILES = {
    "en": "quotes.json",
    "ko": "quotes_ko.json",
    "ja": "quotes_ja.json",
}


@lru_cache(maxsize=8)
def _load_quotes(lang: str = "en") -> list:
    """Load quotes from JSON data file for the given language.

    Falls back to English if the requested language file does not exist.
    """
    data_dir = Path(__file__).parent.parent.parent / "data"
    filename = _LANG_FILES.get(lang, "quotes.json")
    data_path = data_dir / filename

    if not data_path.exists():
        data_path = data_dir / "quotes.json"

    with open(data_path) as f:
        data = json.load(f)
    return data["quotes"]


def get_categories(lang: Optional[str] = None) -> list:
    """Get sorted list of available categories."""
    quotes = _load_quotes(lang or "en")
    return sorted(set(q["category"] for q in quotes))


def get_tags(lang: Optional[str] = None) -> list:
    """Get sorted list of all available tags."""
    quotes = _load_quotes(lang or "en")
    tags = set()
    for q in quotes:
        tags.update(q.get("tags", []))
    return sorted(tags)


def get_quotes_by_category(category: str, lang: Optional[str] = None) -> list:
    """Get all quotes in a category."""
    quotes = _load_quotes(lang or "en")
    return [q for q in quotes if q["category"] == category]


def get_quotes_by_tag(tag: str, lang: Optional[str] = None) -> list:
    """Get all quotes with a specific tag."""
    quotes = _load_quotes(lang or "en")
    return [q for q in quotes if tag in q.get("tags", [])]


def get_quote(category: Optional[str] = None, tag: Optional[str] = None, lang: Optional[str] = None) -> Tuple[str, str]:
    """Get a random quote with optional category/tag filter.

    Uses weighted random selection based on quote weights.
    Returns (quote_text, category).
    """
    quotes = _load_quotes(lang or "en")

    if category and any(q["category"] == category for q in quotes):
        quotes = [q for q in quotes if q["category"] == category]

    if tag:
        filtered = [q for q in quotes if tag in q.get("tags", [])]
        if filtered:
            quotes = filtered

    # Weighted random selection
    selected = _weighted_choice(quotes)
    return selected["text"], selected["category"]


def get_quote_of_the_day(lang: Optional[str] = None) -> Tuple[str, str]:
    """Get deterministic quote of the day based on current date.

    Same date always returns the same quote.
    """
    quotes = _load_quotes(lang or "en")
    today = date.today().isoformat()
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = seed % len(quotes)
    q = quotes[index]
    return q["text"], q["category"]


def _weighted_choice(quotes: list) -> dict:
    """Select a quote using weighted random selection."""
    weights = [q.get("weight", 3) for q in quotes]
    return random.choices(quotes, weights=weights, k=1)[0]
