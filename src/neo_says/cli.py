"""Command-line interface for neo-says."""

import argparse

from neo_says.quotes import get_categories, get_tags, get_quote, get_quote_of_the_day
from neo_says.formatter import format_box


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

    args = parser.parse_args()

    if args.list_categories:
        from neo_says.quotes import get_quotes_by_category
        for cat in get_categories():
            count = len(get_quotes_by_category(cat))
            print(f"  {cat:<15} ({count} quotes)")
        return

    if args.list_tags:
        from neo_says.quotes import get_quotes_by_tag
        for tag in get_tags():
            count = len(get_quotes_by_tag(tag))
            print(f"  {tag:<15} ({count} quotes)")
        return

    if args.today:
        quote, cat = get_quote_of_the_day()
    else:
        quote, cat = get_quote(category=args.category, tag=args.tag)

    if args.raw:
        print(quote)
    else:
        print(format_box(quote))
