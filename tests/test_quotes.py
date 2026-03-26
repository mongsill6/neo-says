"""Tests for quote database and selection."""

from neo_says.quotes import QUOTES, get_quote


class TestQuotes:
    def test_quotes_dict_not_empty(self):
        assert len(QUOTES) > 0

    def test_all_categories_have_quotes(self):
        for cat, quotes in QUOTES.items():
            assert len(quotes) > 0, f"Category '{cat}' has no quotes"

    def test_known_categories_exist(self):
        expected = {"git", "debugging", "meetings", "code-review", "production", "general"}
        assert expected == set(QUOTES.keys())

    def test_get_quote_returns_tuple(self):
        result = get_quote()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_get_quote_with_category(self):
        quote, cat = get_quote("git")
        assert cat == "git"
        assert quote in QUOTES["git"]

    def test_get_quote_random_category(self):
        quote, cat = get_quote()
        assert cat in QUOTES
        assert quote in QUOTES[cat]

    def test_get_quote_invalid_category_falls_back(self):
        quote, cat = get_quote("nonexistent")
        assert cat in QUOTES
        assert quote in QUOTES[cat]

    def test_all_quotes_are_strings(self):
        for cat, quotes in QUOTES.items():
            for q in quotes:
                assert isinstance(q, str)
                assert len(q) > 0
