# API Reference

> "You want an API? Fine. Here it is. Rate-limited, documented, and utterly indifferent to your feelings." -- Neo

Neo Says includes a **FastAPI server** that serves quotes over HTTP. It also has a full Python API for programmatic use. This page covers both.

---

## FastAPI Server

### Starting the Server

```bash
# Default: localhost:8000
uvicorn neo_says.server.app:app

# Custom host and port
uvicorn neo_says.server.app:app --host 0.0.0.0 --port 3000

# With auto-reload for development
uvicorn neo_says.server.app:app --reload

# Production with multiple workers
uvicorn neo_says.server.app:app --host 0.0.0.0 --port 8000 --workers 4
```

Once running, interactive API docs are available at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Rate Limiting

All endpoints are rate-limited to **15 requests per minute** per IP address. Exceed the limit and you'll get a `429 Too Many Requests` response. Neo needs a breather.

### CORS

CORS is fully open (`allow_origins=["*"]`), so you can hit the API from any frontend. Neo doesn't discriminate -- he judges everyone equally.

---

### Endpoints

#### `GET /` -- Welcome

Returns a welcome message and a list of available endpoints. Think of it as the lobby.

```bash
curl http://localhost:8000/
```

```json
{
  "message": "Welcome to Neo Says API. I'd say 'make yourself at home' but I'd rather you didn't.",
  "docs": "/docs",
  "endpoints": [
    "GET /quote",
    "GET /quote/today",
    "GET /quote/{category}",
    "GET /categories",
    "GET /tags",
    "GET /health"
  ]
}
```

---

#### `GET /quote` -- Random Quote

Fetch a random quote. Optionally filter by category, tag, or language. Neo picks. You receive.

**Query Parameters:**

| Parameter  | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| `category` | string | No       | Filter by category name                  |
| `tag`      | string | No       | Filter by tag                            |
| `lang`     | string | No       | Language code: `en`, `ko`, `ja` (default: `en`) |

```bash
# Random quote
curl http://localhost:8000/quote

# Filter by category
curl "http://localhost:8000/quote?category=debugging"

# Filter by tag
curl "http://localhost:8000/quote?tag=truth"

# Japanese quote
curl "http://localhost:8000/quote?lang=ja"

# Category + language
curl "http://localhost:8000/quote?category=debugging&lang=ko"
```

**Response:**

```json
{
  "text": "Your code doesn't need comments. It needs a therapist.",
  "category": "debugging",
  "lang": "en"
}
```

**Error -- invalid category (404):**

```json
{
  "detail": "Category 'nonexistent' doesn't exist. Much like your taste. Try GET /categories for valid options."
}
```

**Error -- unsupported language (400):**

```json
{
  "detail": "Language 'fr' not supported. Try one of ['en', 'ko', 'ja']. Neo speaks many languages, but not that one."
}
```

---

#### `GET /quote/today` -- Quote of the Day

Returns the same quote for the entire day. Deterministic based on the current date -- same date always produces the same quote.

**Query Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `lang`    | string | No       | Language code: `en`, `ko`, `ja` (default: `en`) |

```bash
curl http://localhost:8000/quote/today

# In Korean
curl "http://localhost:8000/quote/today?lang=ko"
```

**Response:**

```json
{
  "text": "There are only two hard things in computer science: cache invalidation, naming things, and off-by-one errors.",
  "category": "programming",
  "lang": "en"
}
```

---

#### `GET /quote/{category}` -- Quote by Category

Get a random quote from a specific category.

**Path Parameters:**

| Parameter  | Type   | Description      |
|------------|--------|------------------|
| `category` | string | Category name    |

**Query Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `lang`    | string | No       | Language code: `en`, `ko`, `ja` (default: `en`) |

```bash
curl http://localhost:8000/quote/debugging

curl "http://localhost:8000/quote/career?lang=ja"
```

**Response:**

```json
{
  "text": "The best debugger ever made is a good night's sleep.",
  "category": "debugging",
  "lang": "en"
}
```

**Error -- unknown category (404):**

```json
{
  "detail": "Category 'doesntexist' not found. Shocking, I know. Try GET /categories to see what actually exists."
}
```

---

#### `GET /categories` -- List Categories

Returns all available quote categories for a given language.

**Query Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `lang`    | string | No       | Language code: `en`, `ko`, `ja` (default: `en`) |

```bash
curl http://localhost:8000/categories

curl "http://localhost:8000/categories?lang=ko"
```

**Response:**

```json
{
  "categories": [
    "career",
    "debugging",
    "lifestyle",
    "programming",
    "tools"
  ]
}
```

---

#### `GET /tags` -- List Tags

Returns all available tags across all quotes.

**Query Parameters:**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `lang`    | string | No       | Language code: `en`, `ko`, `ja` (default: `en`) |

```bash
curl http://localhost:8000/tags

curl "http://localhost:8000/tags?lang=ja"
```

**Response:**

```json
{
  "tags": [
    "career",
    "code-quality",
    "harsh",
    "motivation",
    "reality",
    "truth"
  ]
}
```

---

#### `GET /health` -- Health Check

Check if Neo is alive. Spoiler: Neo is always alive.

```bash
curl http://localhost:8000/health
```

**Response:**

```json
{
  "status": "ok",
  "message": "Neo is alive, mass cynical, and mass ready to judge your life choices."
}
```

---

### Response Models

| Model                | Fields                                    | Used By              |
|----------------------|-------------------------------------------|----------------------|
| `QuoteResponse`      | `text`, `category`, `lang`                | `/quote`, `/quote/today`, `/quote/{category}` |
| `CategoriesResponse` | `categories` (list of strings)            | `/categories`        |
| `TagsResponse`       | `tags` (list of strings)                  | `/tags`              |
| `HealthResponse`     | `status`, `message`                       | `/health`            |
| `WelcomeResponse`    | `message`, `docs`, `endpoints`            | `/`                  |

---

## Python API

You can use Neo Says as a library in your own Python projects. No HTTP server required.

### Quotes Module

```python
from neo_says.quotes import (
    get_quote,
    get_quote_of_the_day,
    get_categories,
    get_tags,
    get_quotes_by_category,
    get_quotes_by_tag,
    SUPPORTED_LANGS,
)
```

#### `get_quote(category=None, tag=None, lang=None) -> tuple[str, str]`

Get a random quote using weighted random selection. Returns `(text, category)`.

```python
text, category = get_quote()
print(f"[{category}] {text}")

# Filter by category
text, cat = get_quote(category="debugging")

# Filter by tag
text, cat = get_quote(tag="truth")

# In Japanese
text, cat = get_quote(lang="ja")
```

#### `get_quote_of_the_day(lang=None) -> tuple[str, str]`

Deterministic quote based on today's date. Same date always returns the same quote (uses MD5 hash of the ISO date string).

```python
text, category = get_quote_of_the_day()
text_ko, cat_ko = get_quote_of_the_day(lang="ko")
```

#### `get_categories(lang=None) -> list[str]`

Get a sorted list of all available categories.

```python
categories = get_categories()       # English
categories = get_categories("ko")   # Korean
```

#### `get_tags(lang=None) -> list[str]`

Get a sorted list of all available tags.

```python
tags = get_tags()
tags = get_tags("ja")
```

#### `get_quotes_by_category(category, lang=None) -> list[dict]`

Get all quotes in a specific category. Returns the raw quote dicts.

```python
quotes = get_quotes_by_category("debugging")
for q in quotes:
    print(q["text"])
```

#### `get_quotes_by_tag(tag, lang=None) -> list[dict]`

Get all quotes with a specific tag.

```python
quotes = get_quotes_by_tag("truth")
```

#### `SUPPORTED_LANGS`

```python
from neo_says.quotes import SUPPORTED_LANGS
print(SUPPORTED_LANGS)
# ['en', 'ko', 'ja']
```

---

### Themes Module

```python
from neo_says.themes import (
    render_quote,
    render_box,
    render_minimal,
    render_ascii_art,
    render_cowsay,
    AVAILABLE_THEMES,
    MAX_WIDTH,
)
```

#### `render_quote(text, author="Neo", theme="box") -> None`

Render and **print** a quote to stdout using the specified theme. Raises `ValueError` for unknown themes.

```python
render_quote("Your code works. I'm as surprised as you are.")
render_quote("Sleep is overrated.", author="The Matrix", theme="cowsay")
```

#### `render_box(text, author="Neo") -> str`

Returns a Rich Panel string with cyan border.

#### `render_minimal(text, author="Neo") -> str`

Returns colored text with no borders.

#### `render_ascii_art(text, author="Neo") -> str`

Returns an ASCII-framed string with ANSI color codes.

#### `render_cowsay(text, author="Neo") -> str`

Returns a speech bubble with the Neo robot character.

All render functions accept `text` and `author` parameters and return a string.

---

### Config Module

```python
from neo_says.config import (
    get_config,
    get_default_theme,
    get_default_author,
    get_default_lang,
    set_config,
    CONFIG_PATH,
)
```

#### `get_config() -> dict`

Load the full configuration from `~/.neo-says.toml`, merged with defaults.

```python
config = get_config()
print(config)
# {'display': {'theme': 'box', 'author': 'Neo'}, 'locale': {'lang': 'auto'}}
```

#### `set_config(key, value) -> None`

Set a config value using dotted key notation and save to disk.

```python
set_config("display.theme", "cowsay")
set_config("display.author", "The Architect")
set_config("locale.lang", "ko")
```

#### Convenience Getters

```python
get_default_theme()   # "box"
get_default_author()  # "Neo"
get_default_lang()    # "auto"
```

---

### Favorites Module

```python
from neo_says.favorites import (
    add_favorite,
    remove_favorite,
    is_favorite,
    load_favorites,
    save_favorites,
    search_favorites,
    get_favorites_by_category,
    clear_favorites,
    get_favorites_path,
)
```

See the [Favorites System](plugins.md#favorites-system) section for usage examples.

---

### Packs Module

```python
from neo_says.packs import (
    install_pack,
    remove_pack,
    list_packs,
    load_pack,
    get_pack_quotes,
    validate_pack,
    PACKS_DIR,
)
```

#### `list_packs() -> list[dict]`

List all installed packs with metadata.

```python
for pack in list_packs():
    print(f"{pack['name']} v{pack['version']} - {pack['quotes_count']} quotes")
```

#### `get_pack_quotes(name=None) -> list[dict]`

Get quotes from a specific pack, or all packs if `name` is `None`.

```python
# All quotes from all packs
all_quotes = get_pack_quotes()

# Quotes from a specific pack
quotes = get_pack_quotes("devops-nightmares")
```

#### `install_pack(source) -> str`

Install a pack from a file path. Returns the pack name.

```python
name = install_pack("./my-pack.yaml")
```

#### `remove_pack(name) -> bool`

Remove an installed pack. Returns `True` if removed, `False` if not found.

---

### TUI Module

```python
from neo_says.tui import run_tui, NeoSaysTUI
```

#### `run_tui() -> None`

Launch the interactive TUI application. This is a blocking call.

```python
run_tui()
```

#### `NeoSaysTUI`

The Textual `App` subclass. Useful if you want to embed or extend the TUI:

```python
app = NeoSaysTUI()
app.run()
```
