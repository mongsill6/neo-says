"""neo-says: A snarky CLI fortune teller for developers."""

__version__ = "3.0.0"

from neo_says.quotes import get_quote, get_quote_of_the_day, get_categories, get_tags
from neo_says.formatter import format_box
from neo_says.themes import AVAILABLE_THEMES, render_quote
from neo_says.config import get_config, get_default_theme, get_default_author
