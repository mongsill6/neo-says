from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    RadioButton,
    RadioSet,
    Static,
)
from textual.reactive import reactive
from textual.message import Message

from neo_says.quotes import _load_quotes, get_categories, SUPPORTED_LANGS
from neo_says.favorites import load_favorites, add_favorite, remove_favorite, is_favorite


class CategoryItem(Static):
    class Selected(Message):
        def __init__(self, category: str | None) -> None:
            super().__init__()
            self.category = category

    def __init__(self, label: str, category: str | None) -> None:
        super().__init__(label)
        self.category = category
        self._label = label

    def on_click(self) -> None:
        self.post_message(self.Selected(self.category))


class QuoteItem(ListItem):
    def __init__(self, quote: dict, favorited: bool) -> None:
        super().__init__()
        self.quote = quote
        self.favorited = favorited

    def compose(self) -> ComposeResult:
        star = "★" if self.favorited else "☆"
        text = self.quote.get("text", "")
        category = self.quote.get("category", "")
        tags = self.quote.get("tags", [])
        tag_str = " ".join(f"#{t}" for t in tags) if tags else ""

        yield Static(f"{star}  {text}", classes="quote-text")
        yield Static(f"[{category}]  {tag_str}", classes="quote-meta")


class NeoSaysTUI(App):
    TITLE = "Neo Says"
    SUB_TITLE = "Quote Browser"

    CSS = """
    Screen {
        background: #0d1117;
        color: #c9d1d9;
    }

    Header {
        background: #161b22;
        color: #58a6ff;
        text-style: bold;
    }

    Footer {
        background: #161b22;
        color: #8b949e;
    }

    #sidebar {
        width: 25%;
        min-width: 20;
        background: #161b22;
        border-right: solid #30363d;
        padding: 1;
    }

    #main {
        width: 75%;
        background: #0d1117;
    }

    .sidebar-title {
        color: #58a6ff;
        text-style: bold;
        margin-bottom: 1;
    }

    RadioSet {
        background: #161b22;
        border: none;
        margin-bottom: 1;
    }

    RadioButton {
        background: #161b22;
        color: #c9d1d9;
    }

    RadioButton:focus {
        background: #1f6feb;
    }

    #categories-container {
        margin-top: 1;
    }

    CategoryItem {
        padding: 0 1;
        color: #c9d1d9;
    }

    CategoryItem:hover {
        background: #21262d;
        color: #58a6ff;
    }

    CategoryItem.active {
        color: #58a6ff;
        text-style: bold;
        background: #1f2937;
    }

    #favorites-btn {
        margin-top: 1;
        padding: 0 1;
        color: #f0c040;
        background: #161b22;
    }

    #favorites-btn:hover {
        background: #21262d;
        color: #ffd700;
    }

    #favorites-btn.active {
        color: #ffd700;
        text-style: bold;
        background: #2d2200;
    }

    #search-input {
        margin: 1;
        background: #21262d;
        border: solid #30363d;
        color: #c9d1d9;
    }

    #search-input:focus {
        border: solid #58a6ff;
    }

    #quotes-list {
        margin: 0 1;
        background: #0d1117;
    }

    ListItem {
        background: #0d1117;
        border-bottom: solid #21262d;
        padding: 1;
    }

    ListItem:hover {
        background: #161b22;
    }

    ListItem.--highlight {
        background: #1f2937;
        border-left: solid #58a6ff;
    }

    .quote-text {
        color: #c9d1d9;
        margin-bottom: 0;
    }

    .quote-meta {
        color: #8b949e;
        text-style: italic;
    }

    #empty-label {
        margin: 2;
        color: #8b949e;
        text-align: center;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("f", "toggle_favorite", "Toggle Favorite"),
        Binding("/", "focus_search", "Search"),
        Binding("tab", "switch_focus", "Switch Panel"),
        Binding("escape", "clear_search", "Clear"),
    ]

    current_lang: reactive[str] = reactive("en")
    current_category: reactive[str | None] = reactive(None)
    show_favorites: reactive[bool] = reactive(False)
    search_query: reactive[str] = reactive("")

    def __init__(self) -> None:
        super().__init__()
        self._all_quotes: list[dict] = []
        self._categories: list[str] = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="body"):
            with Vertical(id="sidebar"):
                yield Static("Language", classes="sidebar-title")
                with RadioSet(id="lang-select"):
                    for lang in SUPPORTED_LANGS:
                        yield RadioButton(lang, value=(lang == "en"))
                yield Static("Categories", classes="sidebar-title")
                with ScrollableContainer(id="categories-container"):
                    yield CategoryItem("All", None)
                with Static(id="favorites-btn"):
                    yield Static("★ Favorites")
            with Vertical(id="main"):
                yield Input(placeholder="Search quotes... (/)", id="search-input")
                yield ListView(id="quotes-list")
        yield Footer()

    def on_mount(self) -> None:
        self._load_data()
        self._refresh_quotes()

    def _load_data(self) -> None:
        self._all_quotes = _load_quotes(lang=self.current_lang)
        self._categories = get_categories(lang=self.current_lang)
        self._rebuild_category_list()

    def _rebuild_category_list(self) -> None:
        container = self.query_one("#categories-container", ScrollableContainer)
        container.remove_children()
        container.mount(CategoryItem("All", None))
        for cat in self._categories:
            container.mount(CategoryItem(cat, cat))
        self._update_active_category()

    def _update_active_category(self) -> None:
        for item in self.query(CategoryItem):
            if item.category is None and not self.show_favorites:
                if self.current_category is None:
                    item.add_class("active")
                else:
                    item.remove_class("active")
            elif item.category == self.current_category and not self.show_favorites:
                item.add_class("active")
            else:
                item.remove_class("active")

        fav_btn = self.query_one("#favorites-btn", Static)
        if self.show_favorites:
            fav_btn.add_class("active")
        else:
            fav_btn.remove_class("active")

    def _get_filtered_quotes(self) -> list[dict]:
        if self.show_favorites:
            favs = {f["text"] for f in load_favorites()}
            quotes = [q for q in self._all_quotes if q.get("text") in favs]
        elif self.current_category is not None:
            quotes = [q for q in self._all_quotes if q.get("category") == self.current_category]
        else:
            quotes = list(self._all_quotes)

        if self.search_query:
            q = self.search_query.lower()
            quotes = [quote for quote in quotes if q in quote.get("text", "").lower()]

        return quotes

    def _refresh_quotes(self) -> None:
        quotes_list = self.query_one("#quotes-list", ListView)
        quotes_list.clear()

        filtered = self._get_filtered_quotes()
        favorited_texts = {f["text"] for f in load_favorites()}

        for quote in filtered:
            fav = quote.get("text", "") in favorited_texts
            quotes_list.append(QuoteItem(quote, fav))

    def on_category_item_selected(self, event: CategoryItem.Selected) -> None:
        self.show_favorites = False
        self.current_category = event.category
        self._update_active_category()
        self._refresh_quotes()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set.id == "lang-select":
            selected = event.index
            if selected < len(SUPPORTED_LANGS):
                self.current_lang = SUPPORTED_LANGS[selected]
                self._load_data()
                self._refresh_quotes()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search-input":
            self.search_query = event.value
            self._refresh_quotes()

    def on_static_click(self, event: Static.Clicked) -> None:
        if event.static.id == "favorites-btn" or (
            event.static.parent and getattr(event.static.parent, "id", None) == "favorites-btn"
        ):
            self.show_favorites = not self.show_favorites
            if self.show_favorites:
                self.current_category = None
            self._update_active_category()
            self._refresh_quotes()

    def action_toggle_favorite(self) -> None:
        quotes_list = self.query_one("#quotes-list", ListView)
        highlighted = quotes_list.highlighted_child
        if highlighted is None or not isinstance(highlighted, QuoteItem):
            return

        quote = highlighted.quote
        text = quote.get("text", "")
        category = quote.get("category", "")
        tags = quote.get("tags", [])

        if is_favorite(text):
            remove_favorite(text)
        else:
            add_favorite(text, category, tags)

        self._refresh_quotes()

    def action_focus_search(self) -> None:
        self.query_one("#search-input", Input).focus()

    def action_clear_search(self) -> None:
        search = self.query_one("#search-input", Input)
        if search.value:
            search.value = ""
            self.search_query = ""
            self._refresh_quotes()
        else:
            self.query_one("#quotes-list", ListView).focus()

    def action_switch_focus(self) -> None:
        focused = self.focused
        if focused is None or isinstance(focused, ListView):
            self.query_one("#search-input", Input).focus()
        elif isinstance(focused, Input):
            self.query_one("#lang-select", RadioSet).focus()
        else:
            self.query_one("#quotes-list", ListView).focus()


def run_tui() -> None:
    app = NeoSaysTUI()
    app.run()
