"""neo-says: A snarky CLI fortune teller for developers."""

__version__ = "2.0.0"

from neo_says.quotes import get_quote, get_quote_of_the_day, get_categories, get_tags
from neo_says.formatter import format_box
