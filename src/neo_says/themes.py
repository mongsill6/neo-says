"""Theme system for the neo-says CLI tool.

Provides multiple visual themes for rendering quotes using the rich library
and plain-text ASCII art.
"""

from __future__ import annotations

import textwrap
from io import StringIO
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

AVAILABLE_THEMES: list[str] = ["box", "minimal", "ascii-art", "cowsay"]

MAX_WIDTH: int = 50


def _wrap(text: str, width: int = MAX_WIDTH) -> str:
    """Word-wrap text to the given width."""
    return "\n".join(textwrap.wrap(text, width=width))


def _wrap_lines(text: str, width: int = MAX_WIDTH) -> list[str]:
    """Word-wrap text and return individual lines."""
    return textwrap.wrap(text, width=width)


# ---------------------------------------------------------------------------
# Theme: box
# ---------------------------------------------------------------------------

def render_box(text: str, author: str = "Neo") -> str:
    """Render a quote inside a rich Panel with a cyan border.

    Args:
        text: The quote body.
        author: Attribution name displayed below the quote.

    Returns:
        The rendered panel as a string.
    """
    wrapped = _wrap(text)
    body = Text()
    body.append(wrapped, style="bold")
    body.append("\n\n")
    body.append(f"-- {author}", style="dim")

    panel = Panel(body, border_style="cyan", width=min(MAX_WIDTH + 6, 60))

    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=60)
    console.print(panel)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Theme: minimal
# ---------------------------------------------------------------------------

def render_minimal(text: str, author: str = "Neo") -> str:
    """Render a quote as simple colored text with no borders.

    Quote text is green, author is dim yellow, separated by an em-dash.

    Args:
        text: The quote body.
        author: Attribution name.

    Returns:
        The rendered text as a string.
    """
    wrapped = _wrap(text)
    body = Text()
    body.append(wrapped, style="green")
    body.append(f" \u2014 ", style="dim")
    body.append(author, style="dim yellow")

    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=60)
    console.print(body)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Theme: ascii-art
# ---------------------------------------------------------------------------

def render_ascii_art(text: str, author: str = "Neo") -> str:
    """Render a quote with an ASCII art border.

    Uses +, -, | characters for the border frame. Quote text is bold white
    and the author line is magenta (represented via ANSI escapes).

    Args:
        text: The quote body.
        author: Attribution name.

    Returns:
        The decorated string with ANSI color codes.
    """
    lines = _wrap_lines(text)
    inner_width = max(len(line) for line in lines) if lines else MAX_WIDTH
    inner_width = max(inner_width, len(f"-- {author}"))

    top = f"+{'-' * (inner_width + 2)}+"
    bottom = top

    bold_white = "\033[1;37m"
    magenta = "\033[35m"
    reset = "\033[0m"

    result: list[str] = [top]
    for line in lines:
        padded = line.ljust(inner_width)
        result.append(f"| {bold_white}{padded}{reset} |")

    result.append(f"| {' ' * inner_width} |")
    author_line = f"-- {author}"
    padded_author = author_line.rjust(inner_width)
    result.append(f"| {magenta}{padded_author}{reset} |")
    result.append(bottom)

    return "\n".join(result) + "\n"


# ---------------------------------------------------------------------------
# Theme: cowsay
# ---------------------------------------------------------------------------

def render_cowsay(text: str, author: str = "Neo") -> str:
    """Render a quote as a Neo-style cowsay speech bubble with ASCII robot.

    Args:
        text: The quote body.
        author: Attribution name.

    Returns:
        The decorated speech bubble and character as a plain string.
    """
    lines = _wrap_lines(text)
    lines.append(f"-- {author}")

    inner_width = max(len(line) for line in lines) if lines else MAX_WIDTH

    result: list[str] = []
    result.append(f" {'_' * (inner_width + 2)}")

    if len(lines) == 1:
        result.append(f"< {lines[0].ljust(inner_width)} >")
    else:
        for i, line in enumerate(lines):
            padded = line.ljust(inner_width)
            if i == 0:
                result.append(f"/ {padded} \\")
            elif i == len(lines) - 1:
                result.append(f"\\ {padded} /")
            else:
                result.append(f"| {padded} |")

    result.append(f" {'-' * (inner_width + 2)}")

    # Neo-style matrix robot character
    character = (
        "        \\",
        "         \\",
        "          \\  ",
        "           [O_O]",
        "           /|__|\\",
        "            |  |",
        "           _/  \\_",
    )
    result.extend(character)

    return "\n".join(result) + "\n"


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def render_quote(text: str, author: str = "Neo", theme: str = "box") -> None:
    """Render and print a quote using the specified theme.

    For rich-based themes (box, minimal), output is printed via a rich
    Console. For plain-text themes (ascii-art, cowsay), standard print
    is used.

    Args:
        text: The quote body.
        author: Attribution name.
        theme: One of the available theme names.

    Raises:
        ValueError: If the theme name is not recognized.
    """
    if theme not in AVAILABLE_THEMES:
        raise ValueError(
            f"Unknown theme '{theme}'. "
            f"Available themes: {', '.join(AVAILABLE_THEMES)}"
        )

    renderers = {
        "box": render_box,
        "minimal": render_minimal,
        "ascii-art": render_ascii_art,
        "cowsay": render_cowsay,
    }

    rendered = renderers[theme](text, author)

    if theme in ("box", "minimal"):
        console = Console()
        console.print(rendered, end="", highlight=False)
    else:
        print(rendered, end="")
