"""Quote database and selection logic."""

import json
import hashlib
import random
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple


def _load_quotes() -> list:
    """Load quotes from JSON data file."""
    data_path = Path(__file__).parent.parent.parent / "data" / "quotes.json"
    with open(data_path) as f:
        data = json.load(f)
    return data["quotes"]


def get_categories() -> list:
    """Get sorted list of available categories."""
    quotes = _load_quotes()
    return sorted(set(q["category"] for q in quotes))


def get_tags() -> list:
    """Get sorted list of all available tags."""
    quotes = _load_quotes()
    tags = set()
    for q in quotes:
        tags.update(q.get("tags", []))
    return sorted(tags)


def get_quotes_by_category(category: str) -> list:
    """Get all quotes in a category."""
    quotes = _load_quotes()
    return [q for q in quotes if q["category"] == category]


def get_quotes_by_tag(tag: str) -> list:
    """Get all quotes with a specific tag."""
    quotes = _load_quotes()
    return [q for q in quotes if tag in q.get("tags", [])]


def get_quote(category: Optional[str] = None, tag: Optional[str] = None) -> Tuple[str, str]:
    """Get a random quote with optional category/tag filter.

    Uses weighted random selection based on quote weights.
    Returns (quote_text, category).
    """
    quotes = _load_quotes()

    if category and any(q["category"] == category for q in quotes):
        quotes = [q for q in quotes if q["category"] == category]

    if tag:
        filtered = [q for q in quotes if tag in q.get("tags", [])]
        if filtered:
            quotes = filtered

    # Weighted random selection
    selected = _weighted_choice(quotes)
    return selected["text"], selected["category"]


def get_quote_of_the_day() -> Tuple[str, str]:
    """Get deterministic quote of the day based on current date.

    Same date always returns the same quote.
    """
    quotes = _load_quotes()
    today = date.today().isoformat()
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = seed % len(quotes)
    q = quotes[index]
    return q["text"], q["category"]


def _weighted_choice(quotes: list) -> dict:
    """Select a quote using weighted random selection."""
    weights = [q.get("weight", 3) for q in quotes]
    return random.choices(quotes, weights=weights, k=1)[0]
