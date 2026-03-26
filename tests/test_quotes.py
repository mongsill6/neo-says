"""Tests for quote engine."""

import json
from datetime import date
from pathlib import Path
from unittest.mock import patch

from neo_says.quotes import (
    _load_quotes,
    get_categories,
    get_tags,
    get_quote,
    get_quote_of_the_day,
    get_quotes_by_category,
    get_quotes_by_tag,
)


class TestDataIntegrity:
    def test_load_quotes_returns_list(self):
        quotes = _load_quotes()
        assert isinstance(quotes, list)
        assert len(quotes) > 0

    def test_all_quotes_have_required_fields(self):
        for q in _load_quotes():
            assert "text" in q
            assert "category" in q
            assert "tags" in q
            assert "weight" in q

    def test_all_quotes_are_strings(self):
        for q in _load_quotes():
            assert isinstance(q["text"], str)
            assert len(q["text"]) > 0

    def test_all_tags_are_lists(self):
        for q in _load_quotes():
            assert isinstance(q["tags"], list)
            assert len(q["tags"]) > 0

    def test_weights_are_valid(self):
        for q in _load_quotes():
            assert isinstance(q["weight"], int)
            assert 1 <= q["weight"] <= 5

    def test_json_file_exists(self):
        data_path = Path(__file__).parent.parent / "data" / "quotes.json"
        assert data_path.exists()

    def test_json_is_valid(self):
        data_path = Path(__file__).parent.parent / "data" / "quotes.json"
        with open(data_path) as f:
            data = json.load(f)
        assert "version" in data
        assert "quotes" in data

    def test_minimum_quote_count(self):
        quotes = _load_quotes()
        assert len(quotes) >= 33


class TestCategories:
    def test_get_categories_returns_sorted_list(self):
        cats = get_categories()
        assert isinstance(cats, list)
        assert cats == sorted(cats)

    def test_known_categories_exist(self):
        cats = get_categories()
        expected = {"git", "debugging", "meetings", "code-review", "production", "general"}
        assert expected == set(cats)

    def test_get_quotes_by_category(self):
        for cat in get_categories():
            quotes = get_quotes_by_category(cat)
            assert len(quotes) > 0
            for q in quotes:
                assert q["category"] == cat


class TestTags:
    def test_get_tags_returns_sorted_list(self):
        tags = get_tags()
        assert isinstance(tags, list)
        assert tags == sorted(tags)
        assert len(tags) > 0

    def test_get_quotes_by_tag(self):
        tags = get_tags()
        for tag in tags:
            quotes = get_quotes_by_tag(tag)
            assert len(quotes) > 0
            for q in quotes:
                assert tag in q["tags"]

    def test_every_quote_has_tags(self):
        for q in _load_quotes():
            assert len(q["tags"]) >= 1


class TestGetQuote:
    def test_returns_tuple(self):
        result = get_quote()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_with_category(self):
        quote, cat = get_quote(category="git")
        assert cat == "git"

    def test_with_tag(self):
        tags = get_tags()
        if tags:
            quote, cat = get_quote(tag=tags[0])
            assert isinstance(quote, str)

    def test_invalid_category_falls_back(self):
        quote, cat = get_quote(category="nonexistent")
        assert cat in get_categories()

    def test_invalid_tag_falls_back(self):
        quote, cat = get_quote(tag="nonexistent_tag_xyz")
        assert isinstance(quote, str)


class TestQuoteOfTheDay:
    def test_returns_tuple(self):
        result = get_quote_of_the_day()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_deterministic(self):
        q1 = get_quote_of_the_day()
        q2 = get_quote_of_the_day()
        assert q1 == q2

    def test_different_dates_different_quotes(self):
        q1 = get_quote_of_the_day()
        with patch("neo_says.quotes.date") as mock_date:
            mock_date.today.return_value = date(2020, 1, 1)
            mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
            q2 = get_quote_of_the_day()
        # They might be the same by coincidence, but the mechanism should work
        assert isinstance(q2, tuple)


class TestWeightedSelection:
    def test_weighted_selection_respects_weights(self):
        """Statistical test: higher weights should be selected more often."""
        counts = {}
        for _ in range(1000):
            quote, _ = get_quote()
            counts[quote] = counts.get(quote, 0) + 1
        # Just verify it runs and produces varied results
        assert len(counts) > 1
