"""Command-line interface for neo-says."""

import argparse

from neo_says.quotes import QUOTES, get_quote
from neo_says.formatter import format_box


def main():
    """Entry point for the neo-says CLI."""
    parser = argparse.ArgumentParser(
        description="Snarky developer wisdom from Neo."
    )
    parser.add_argument(
        "-c", "--category",
        choices=list(QUOTES.keys()),
        help="Filter quotes by category",
    )
    parser.add_argument(
        "-l", "--list-categories",
        action="store_true",
        help="List available categories",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print without the box (for piping)",
    )

    args = parser.parse_args()

    if args.list_categories:
        for cat, quotes in QUOTES.items():
            print(f"  {cat:<15} ({len(quotes)} quotes)")
        return

    quote, cat = get_quote(args.category)

    if args.raw:
        print(quote)
    else:
        print(format_box(quote))
