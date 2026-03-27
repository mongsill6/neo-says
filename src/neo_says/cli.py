"""Command-line interface for neo-says."""

import argparse
import os
import re
import sys

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


def _handle_pack_command(args) -> None:
    """Handle the 'pack' subcommand."""
    from neo_says.packs import install_pack, list_packs, remove_pack

    if args.pack_action == "list":
        packs = list_packs()
        if not packs:
            print("No packs installed.")
            print("Install one with: neo-says pack install <file.yaml>")
            return
        print(f"Installed packs ({len(packs)}):\n")
        for p in packs:
            print(f"  {p['name']:<20} v{p['version']:<8} ({p['quotes_count']} quotes)")
            if p['description']:
                print(f"  {'':20} {p['description']}")
            print()

    elif args.pack_action == "install":
        try:
            name = install_pack(args.file)
            print(f"Pack '{name}' installed successfully.")
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.pack_action == "remove":
        if remove_pack(args.name):
            print(f"Pack '{args.name}' removed.")
        else:
            print(f"Pack '{args.name}' not found.", file=sys.stderr)
            sys.exit(1)

    else:
        print("Usage: neo-says pack {install|list|remove}")
        sys.exit(1)


def main():
    """Entry point for the neo-says CLI."""
    parser = argparse.ArgumentParser(
        description="Snarky developer wisdom from Neo."
    )
    subparsers = parser.add_subparsers(dest="command")

    # TUI subcommand
    subparsers.add_parser("tui", help="Launch interactive TUI browser")

    # Pack subcommand
    pack_parser = subparsers.add_parser("pack", help="Manage quote packs")
    pack_sub = pack_parser.add_subparsers(dest="pack_action")

    pack_sub.add_parser("list", help="List installed packs")

    pack_install = pack_sub.add_parser("install", help="Install a quote pack")
    pack_install.add_argument("file", help="Path to YAML pack file")

    pack_remove = pack_sub.add_parser("remove", help="Remove a quote pack")
    pack_remove.add_argument("name", help="Pack name to remove")

    # Main options
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
    parser.add_argument(
        "--pack",
        default=None,
        help="Use quotes from a pack (name or 'all' for all packs)",
    )

    args = parser.parse_args()

    # Handle subcommands
    if args.command == "tui":
        from neo_says.tui import run_tui
        run_tui()
        return

    if args.command == "pack":
        _handle_pack_command(args)
        return

    # Handle config setters
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

    # Handle --pack option
    if args.pack:
        import random
        from neo_says.packs import get_pack_quotes
        try:
            pack_name = None if args.pack == "all" else args.pack
            quotes = get_pack_quotes(pack_name)
            if not quotes:
                print("No quotes found in pack(s).", file=sys.stderr)
                sys.exit(1)
            weights = [q.get("weight", 3) for q in quotes]
            selected = random.choices(quotes, weights=weights, k=1)[0]
            theme = args.theme or get_default_theme()
            author = get_default_author()
            if args.raw:
                print(selected["text"])
            else:
                render_quote(selected["text"], author=author, theme=theme)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
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
