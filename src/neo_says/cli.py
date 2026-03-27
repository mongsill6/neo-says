"""Command-line interface for neo-says."""

import argparse
import os
import re

from neo_says.quotes import get_categories, get_tags, get_quote, get_quote_of_the_day, SUPPORTED_LANGS
from neo_says.themes import AVAILABLE_THEMES, render_quote
from neo_says.config import get_default_theme, get_default_author, get_default_lang, set_config


def detect_lang(cli_arg=None) -> str:
    """Detect the language to use.

    Priority order:
    1. CLI --lang argument
    2. Config file locale.lang (if not 'auto')
    3. LANG environment variable
    4. Fallback to 'en'
    """
    if cli_arg is not None:
        return cli_arg

    configured = get_default_lang()
    if configured and configured != "auto":
        return configured

    env_lang = os.environ.get("LANG", "")
    if env_lang:
        match = re.match(r"([a-z]{2})(?:_[A-Z]{2})?", env_lang)
        if match:
            lang_code = match.group(1)
            if lang_code in SUPPORTED_LANGS:
                return lang_code

    return "en"


def main():
    """Entry point for the neo-says CLI."""
    parser = argparse.ArgumentParser(
        description="Snarky developer wisdom from Neo."
    )
    parser.add_argument(
        "-c", "--category",
        help="Filter quotes by category",
    )
    parser.add_argument(
        "-t", "--tag",
        help="Filter quotes by tag",
    )
    parser.add_argument(
        "-l", "--list-categories",
        action="store_true",
        help="List available categories",
    )
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="List available tags",
    )
    parser.add_argument(
        "--today",
        action="store_true",
        help="Show the quote of the day",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print without the box (for piping)",
    )
    parser.add_argument(
        "--theme",
        choices=AVAILABLE_THEMES,
        default=None,
        help="Display theme (box, minimal, ascii-art, cowsay)",
    )
    parser.add_argument(
        "--set-theme",
        choices=AVAILABLE_THEMES,
        help="Set default theme and save to config",
    )
    parser.add_argument(
        "--lang",
        choices=SUPPORTED_LANGS,
        default=None,
        help="Language for quotes (en, ko, ja)",
    )
    parser.add_argument(
        "--set-lang",
        choices=SUPPORTED_LANGS,
        help="Set default language and save to config",
    )

    args = parser.parse_args()

    if args.set_theme:
        set_config("display.theme", args.set_theme)
        print(f"Default theme set to: {args.set_theme}")
        return

    if args.set_lang:
        set_config("locale.lang", args.set_lang)
        print(f"Default language set to: {args.set_lang}")
        return

    lang = detect_lang(args.lang)

    if args.list_categories:
        from neo_says.quotes import get_quotes_by_category
        for cat in get_categories(lang=lang):
            count = len(get_quotes_by_category(cat, lang=lang))
            print(f"  {cat:<15} ({count} quotes)")
        return

    if args.list_tags:
        from neo_says.quotes import get_quotes_by_tag
        for tag in get_tags(lang=lang):
            count = len(get_quotes_by_tag(tag, lang=lang))
            print(f"  {tag:<15} ({count} quotes)")
        return

    if args.today:
        quote, cat = get_quote_of_the_day(lang=lang)
    else:
        quote, cat = get_quote(category=args.category, tag=args.tag, lang=lang)

    theme = args.theme or get_default_theme()
    author = get_default_author()

    if args.raw:
        print(quote)
    else:
        render_quote(quote, author=author, theme=theme)
