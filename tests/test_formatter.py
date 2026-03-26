"""Tests for output formatting."""

from neo_says.formatter import format_box


class TestFormatBox:
    def test_returns_string(self):
        result = format_box("Hello world")
        assert isinstance(result, str)

    def test_contains_text(self):
        result = format_box("Test quote here")
        assert "Test quote here" in result

    def test_has_box_borders(self):
        result = format_box("Hello")
        assert "╭" in result
        assert "╰" in result
        assert "│" in result

    def test_default_author(self):
        result = format_box("Hello")
        assert "— Neo" in result

    def test_custom_author(self):
        result = format_box("Hello", author="Test")
        assert "— Test" in result

    def test_long_text_wraps(self):
        long_text = "This is a very long quote that should definitely wrap across multiple lines in the box"
        result = format_box(long_text)
        lines = result.split("\n")
        assert len(lines) > 3  # top border + at least 2 content lines + author + bottom border

    def test_box_lines_same_width(self):
        result = format_box("Test quote")
        lines = result.split("\n")
        # All lines between top and bottom border should have same visual width
        content_lines = lines[1:-1]
        lengths = [len(line) for line in content_lines]
        assert len(set(lengths)) == 1
