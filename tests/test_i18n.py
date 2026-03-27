"""Tests for i18n / locale support."""

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from neo_says.quotes import (
    _load_quotes,
    get_categories,
    get_tags,
    get_quote,
    get_quote_of_the_day,
    get_quotes_by_category,
    SUPPORTED_LANGS,
)


class TestSupportedLangs:
    def test_supported_langs_list(self):
        assert "en" in SUPPORTED_LANGS
        assert "ko" in SUPPORTED_LANGS
        assert "ja" in SUPPORTED_LANGS

    def test_all_lang_files_exist(self):
        data_dir = Path(__file__).parent.parent / "data"
        assert (data_dir / "quotes.json").exists()
        assert (data_dir / "quotes_ko.json").exists()
        assert (data_dir / "quotes_ja.json").exists()


class TestKoreanQuotes:
    def test_load_korean_quotes(self):
        quotes = _load_quotes(lang="ko")
        assert isinstance(quotes, list)
        assert len(quotes) >= 30

    def test_korean_quotes_have_required_fields(self):
        for q in _load_quotes(lang="ko"):
            assert "text" in q
            assert "category" in q
            assert "tags" in q
            assert "weight" in q

    def test_korean_categories_match_english(self):
        en_cats = set(get_categories(lang="en"))
        ko_cats = set(get_categories(lang="ko"))
        assert en_cats == ko_cats

    def test_korean_quote_selection(self):
        quote, cat = get_quote(lang="ko")
        assert isinstance(quote, str)
        assert len(quote) > 0

    def test_korean_quote_of_the_day(self):
        q1 = get_quote_of_the_day(lang="ko")
        q2 = get_quote_of_the_day(lang="ko")
        assert q1 == q2

    def test_korean_category_filter(self):
        quote, cat = get_quote(category="git", lang="ko")
        assert cat == "git"


class TestJapaneseQuotes:
    def test_load_japanese_quotes(self):
        quotes = _load_quotes(lang="ja")
        assert isinstance(quotes, list)
        assert len(quotes) >= 20

    def test_japanese_quotes_have_required_fields(self):
        for q in _load_quotes(lang="ja"):
            assert "text" in q
            assert "category" in q
            assert "tags" in q
            assert "weight" in q

    def test_japanese_categories_match_english(self):
        en_cats = set(get_categories(lang="en"))
        ja_cats = set(get_categories(lang="ja"))
        assert en_cats == ja_cats

    def test_japanese_quote_selection(self):
        quote, cat = get_quote(lang="ja")
        assert isinstance(quote, str)
        assert len(quote) > 0


class TestLangFallback:
    def test_unsupported_lang_falls_back_to_english(self):
        quotes = _load_quotes(lang="fr")
        en_quotes = _load_quotes(lang="en")
        assert quotes == en_quotes

    def test_none_lang_defaults_to_english(self):
        quotes = _load_quotes(lang=None)
        en_quotes = _load_quotes(lang="en")
        assert quotes == en_quotes


class TestAutoDetection:
    """Test LANG environment variable detection via CLI."""

    def _run(self, *args, env_override=None):
        env = {"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""}
        if env_override:
            env.update(env_override)
        return subprocess.run(
            [sys.executable, "-m", "neo_says", *args],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env=env,
        )

    def test_lang_flag_en(self):
        result = self._run("--lang", "en", "--raw")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_lang_flag_ko(self):
        result = self._run("--lang", "ko", "--raw")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_lang_flag_ja(self):
        result = self._run("--lang", "ja", "--raw")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_list_categories_with_lang(self):
        result = self._run("--lang", "ko", "--list-categories")
        assert result.returncode == 0
        assert "git" in result.stdout
