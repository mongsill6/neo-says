import pytest

from neo_says.themes import (
    AVAILABLE_THEMES,
    render_ascii_art,
    render_box,
    render_cowsay,
    render_minimal,
    render_quote,
)


def test_available_themes():
    for theme in ["box", "minimal", "ascii-art", "cowsay"]:
        assert theme in AVAILABLE_THEMES


def test_render_box_contains_quote():
    result = render_box("Stay hungry, stay foolish")
    assert "Stay hungry, stay foolish" in result


def test_render_minimal_contains_quote():
    result = render_minimal("The Matrix has you")
    assert "The Matrix has you" in result


def test_render_ascii_art_contains_quote():
    result = render_ascii_art("Follow the white rabbit")
    assert "Follow the white rabbit" in result
    assert "+" in result
    assert "-" in result
    assert "|" in result


def test_render_cowsay_contains_quote():
    result = render_cowsay("There is no spoon")
    assert "There is no spoon" in result


def test_render_quote_invalid_theme():
    with pytest.raises(ValueError):
        render_quote("hello", theme="nonexistent")


def test_render_all_themes_have_author():
    author = "Morpheus"
    for fn in [render_box, render_minimal, render_ascii_art, render_cowsay]:
        result = fn("Wake up", author=author)
        assert author in result


def test_long_quote_wrapping():
    long_text = "A" * 500
    for fn in [render_box, render_minimal, render_ascii_art, render_cowsay]:
        result = fn(long_text)
        assert "A" in result
