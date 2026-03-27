# Contributing to neo-says

So, you want to contribute to neo-says? How *refreshingly* optimistic of you.
Don't worry -- we won't judge your code. Much.

Kidding. We actually love contributions. Whether it's a new quote, a theme, a bug fix,
or a whole new feature, you're welcome here. Just follow the guidelines below and
we'll get along just fine.

---

## Development Setup

### Prerequisites

- Python 3.8 or higher (3.11+ recommended)
- Git
- A terminal you're not afraid to use

### Getting Started

```bash
# Clone the repo (you know the drill)
git clone https://github.com/mongsill6/neo-says.git
cd neo-says

# Create a virtual environment (because global installs are chaos)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

That's it. You now have `neo-says` available as a CLI command, and any changes
you make to the source will take effect immediately. Magic? No, just editable installs.

---

## Project Structure

Here's the lay of the land:

```
neo-says/
├── src/neo_says/          # Main package
│   ├── __init__.py
│   ├── __main__.py        # python -m neo_says entry point
│   ├── cli.py             # CLI argument parsing & dispatch
│   ├── config.py          # User config (~/.neo-says.toml)
│   ├── favorites.py       # Favorite quotes management
│   ├── formatter.py       # Quote text formatting utilities
│   ├── packs.py           # YAML quote pack system
│   ├── quotes.py          # Quote database & selection logic
│   ├── themes.py          # Visual theme rendering (box, minimal, ascii-art, cowsay)
│   ├── tui.py             # Interactive TUI browser (Textual)
│   └── server/            # REST API server (FastAPI)
│       ├── __init__.py
│       ├── __main__.py
│       └── app.py
├── data/                  # Quote databases
│   ├── quotes.json        # English quotes
│   ├── quotes_ko.json     # Korean quotes
│   └── quotes_ja.json     # Japanese quotes
├── tests/                 # Test suite
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_favorites.py
│   ├── test_formatter.py
│   ├── test_i18n.py
│   ├── test_packs.py
│   ├── test_quotes.py
│   ├── test_server.py
│   ├── test_themes.py
│   └── test_tui.py
├── docs/                  # Documentation (MkDocs Material)
├── scripts/               # Utility scripts
├── .github/workflows/     # CI/CD pipelines
├── pyproject.toml         # Build config & dependencies
└── mkdocs.yml             # Docs site config
```

---

## How to Add Quotes

Quotes live in JSON files under `data/`. Each quote entry has this structure:

```json
{
  "text": "Your commit message says 'minor fix'. The diff is 847 lines.",
  "category": "git",
  "tags": ["humor", "relatable", "truth"],
  "weight": 5
}
```

### Fields

| Field      | Type       | Required | Description                                      |
|------------|------------|----------|--------------------------------------------------|
| `text`     | string     | Yes      | The quote itself                                  |
| `category` | string     | Yes      | Category (e.g., `git`, `debugging`, `meetings`)   |
| `tags`     | list[str]  | Yes      | Tags for filtering (e.g., `humor`, `wisdom`)      |
| `weight`   | int (1-5)  | Yes      | Selection probability weight (5 = most frequent)  |

### Steps

1. Open the appropriate file in `data/`:
    - English: `quotes.json`
    - Korean: `quotes_ko.json`
    - Japanese: `quotes_ja.json`
2. Add your quote to the `"quotes"` array.
3. Make sure your category is consistent with existing ones (run `neo-says -l` to list them).
4. Run the tests: `pytest tests/test_quotes.py -v`
5. Submit a PR. We like PRs.

### Guidelines for Good Quotes

- Keep it snarky but not mean-spirited. We roast code, not people.
- Developer-relatable humor scores high.
- Avoid quotes that are just... factual statements. This isn't a textbook.
- Weight 3 is the default. Use 4-5 for absolute bangers, 1-2 for niche material.

---

## How to Create Themes

Themes control how quotes are visually rendered in the terminal. The existing themes
are defined in `src/neo_says/themes.py`.

### Current Themes

- **box** -- Rich panel with a styled border (the default, because we have standards)
- **minimal** -- Clean text with subtle formatting
- **ascii-art** -- Old-school ASCII box art
- **cowsay** -- Because some traditions must be honored

### Adding a New Theme

1. Open `src/neo_says/themes.py`.
2. Add your theme name to the `AVAILABLE_THEMES` list:
   ```python
   AVAILABLE_THEMES: list[str] = ["box", "minimal", "ascii-art", "cowsay", "your-theme"]
   ```
3. Create a render function following the pattern of existing themes:
   ```python
   def _render_your_theme(text: str, author: str, width: int = MAX_WIDTH) -> str:
       """Render quote in your custom style."""
       lines = _wrap_lines(text, width)
       # Build your formatted output here
       return output
   ```
4. Wire it into the main `render_quote()` dispatcher.
5. Add tests in `tests/test_themes.py`.

---

## How to Write Packs

Packs are YAML-based quote collections that users can install separately. They let
anyone extend neo-says without modifying the core quote database.

### Pack Format

Create a YAML file with this structure:

```yaml
name: devops-nightmares
version: "1.0.0"
description: "Quotes from the production incident trenches"
author: your-github-username

quotes:
  - text: "It works on my machine. Ship the machine."
    category: devops
    tags: [humor, classic]
    weight: 5
  - text: "DNS: it's always DNS."
    category: devops
    tags: [truth, wisdom]
    weight: 4
```

### Required Fields

| Field     | Type   | Description              |
|-----------|--------|--------------------------|
| `name`    | string | Unique pack identifier   |
| `version` | string | Semantic version         |
| `quotes`  | list   | Array of quote objects   |

Each quote must have a `text` field at minimum. `category`, `tags`, and `weight`
are optional but recommended.

### Installing & Testing a Pack

```bash
# Install your pack
neo-says pack install my-pack.yaml

# List installed packs
neo-says pack list

# Use quotes from your pack
neo-says --pack my-pack

# Use quotes from all installed packs
neo-says --pack all

# Remove when done testing
neo-says pack remove my-pack
```

Packs are stored in `~/.neo-says/packs/`.

---

## Testing Guide

We use [pytest](https://docs.pytest.org/) and we take testing seriously.
Not "write tests after the fact" seriously -- *actually* seriously.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output (recommended for development)
pytest -v

# Run a specific test file
pytest tests/test_themes.py -v

# Run a specific test function
pytest tests/test_quotes.py::test_get_quote_returns_string -v

# Run tests matching a keyword
pytest -k "theme" -v
```

### Test Structure

Each module has a corresponding test file:

| Module         | Test File           | What It Tests                        |
|----------------|---------------------|--------------------------------------|
| `cli.py`       | `test_cli.py`       | CLI argument parsing, subcommands    |
| `config.py`    | `test_config.py`    | Config read/write, defaults          |
| `favorites.py` | `test_favorites.py` | Favorite add/remove/list             |
| `formatter.py` | `test_formatter.py` | Text formatting, wrapping            |
| `quotes.py`    | `test_quotes.py`    | Quote loading, filtering, selection  |
| `themes.py`    | `test_themes.py`    | Theme rendering, all theme variants  |
| `packs.py`     | `test_packs.py`     | Pack install/validate/remove         |
| `tui.py`       | `test_tui.py`       | TUI application behavior             |
| `server/`      | `test_server.py`    | REST API endpoints                   |
| `quotes.py`    | `test_i18n.py`      | Multi-language quote loading         |

### Writing Tests

- Follow the existing patterns in the test files.
- Use descriptive test names: `test_cowsay_theme_renders_bubble` not `test_theme_3`.
- Use `tmp_path` fixture for any file I/O.
- Mock external state (home directory, config files) to keep tests isolated.

---

## CI/CD Pipeline

We run three GitHub Actions workflows. Here's what each one does:

### CI (`ci.yml`) -- Every Push & PR

Runs on every push to `main` and on all pull requests.

- **Matrix testing**: Python 3.9, 3.10, 3.11, 3.12
- **Linting**: `flake8 src/ tests/` -- catches style issues and obvious bugs
- **Type checking**: `mypy src/neo_says/ --ignore-missing-imports` -- keeps types honest
- **Tests**: `pytest -v --tb=short` -- the full test suite

Your PR must pass all of these. No exceptions. (Well, maybe one exception,
but it better be a good one.)

### Docs (`docs.yml`) -- On Docs Changes

Triggered when files in `docs/` or `mkdocs.yml` are modified on `main`.

- Builds the MkDocs Material site
- Deploys to GitHub Pages via `mkdocs gh-deploy`

### Publish (`publish.yml`) -- On Version Tags

Triggered when a tag matching `v*` is pushed (e.g., `v7.0.0`).

- Builds the distribution with `python -m build`
- Publishes to PyPI via trusted publishing

---

## Code Style Guidelines

### Formatting & Linting

- **Line length**: 88 characters (configured in `pyproject.toml` via ruff)
- **Target**: Python 3.8+ compatibility
- **Linter**: flake8 (enforced in CI)
- **Type checker**: mypy (enforced in CI)
- **Formatter**: ruff (recommended, not enforced... yet)

### General Rules

- Use type hints. Not every variable, but function signatures at minimum.
- Docstrings on all public functions and classes (Google style preferred).
- No wildcard imports (`from module import *`). We're not barbarians.
- Keep functions focused. If a function needs a "Part 2" comment, it needs a refactor.
- Prefer `pathlib.Path` over `os.path` for filesystem operations.

### Import Order

```python
# Standard library
import json
import sys
from pathlib import Path

# Third-party
from rich.console import Console
import yaml

# Local
from neo_says.quotes import get_quote
from neo_says.themes import render_quote
```

---

## PR Process

### Before Submitting

1. **Branch**: Create a feature branch from `main`:
   ```bash
   git checkout -b feature/my-awesome-thing
   ```
2. **Code**: Make your changes, following the style guidelines above.
3. **Test**: Run the full test suite and make sure everything passes:
   ```bash
   pytest -v
   ```
4. **Lint**: Check your code passes linting:
   ```bash
   flake8 src/ tests/
   mypy src/neo_says/ --ignore-missing-imports
   ```

### PR Guidelines

- **Title**: Keep it clear and concise. "Add cowsay theme variant" not "stuff".
- **Description**: Explain *what* and *why*. If it fixes an issue, reference it.
- **Size**: Smaller is better. A 50-line PR gets reviewed today. A 500-line PR gets
  reviewed... eventually.
- **One thing**: Each PR should do one thing. Adding quotes AND refactoring the theme
  engine? That's two PRs.

### Review Process

1. Open your PR against `main`.
2. CI will run automatically -- make sure it's green.
3. A maintainer will review your code.
4. Address any feedback (we don't bite, promise).
5. Once approved, it gets squash-merged.

---

## Questions?

Open an issue on GitHub. Or, if you're feeling adventurous, just submit a PR and
we'll figure it out together.

Welcome aboard. Neo approves. Probably.
