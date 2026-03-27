# neo-says

[![CI](https://github.com/mongsill6/neo-says/actions/workflows/ci.yml/badge.svg)](https://github.com/mongsill6/neo-says/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/neo-says.svg)](https://pypi.org/project/neo-says/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/mongsill6/neo-says/blob/main/LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://pypi.org/project/neo-says/)

**A snarky CLI fortune teller for developers.**

neo-says delivers developer wisdom with attitude. Think `fortune` but with
opinions about your git habits, debugging rituals, and meeting survival strategies.

```
╭──────────────────────────────────────────────────╮
│                                                  │
│  Your commit message says 'minor fix'.           │
│  The diff is 847 lines.                          │
│                                                  │
│                              — Neo               │
╰──────────────────────────────────────────────────╯
```

---

## Quick Install

```bash
pip install neo-says
```

## Quick Start

```bash
neo-says                    # Random snarky developer quote
neo-says --today            # Quote of the day
neo-says -c git             # Git-themed roast
neo-says --theme cowsay     # Moo with attitude
neo-says --lang ko          # Korean quotes
neo-says tui                # Interactive TUI browser
```

---

## Features

### Multiple Themes

Four built-in visual themes to match your terminal aesthetic:

- **box** -- Clean Rich panel with a styled border (default)
- **minimal** -- Subtle, no-nonsense formatting
- **ascii-art** -- Retro ASCII box for the old-school crowd
- **cowsay** -- Because tradition matters

```bash
neo-says --theme ascii-art
neo-says --set-theme minimal   # Set your default
```

### Internationalization (i18n)

Quotes available in three languages with automatic locale detection:

- English (`en`)
- Korean (`ko`)
- Japanese (`ja`)

```bash
neo-says --lang ja
neo-says --set-lang ko   # Set your default
```

### Interactive TUI Browser

A full terminal UI built with [Textual](https://textual.textualize.io/) for
browsing, filtering, and favoriting quotes:

```bash
neo-says tui
```

### REST API Server

Serve quotes over HTTP with FastAPI. Built-in rate limiting included:

```bash
pip install neo-says[server]
python -m neo_says.server
# GET http://localhost:8000/quote
```

### Quote Packs

Extend neo-says with community YAML quote packs:

```bash
neo-says pack install devops-nightmares.yaml
neo-says --pack devops-nightmares
neo-says pack list
```

### Shell Integration

Add neo-says to your MOTD or shell startup for daily wisdom:

```bash
# Add to ~/.bashrc or ~/.zshrc
neo-says --today
```

### Favorites System

Save and recall the quotes that hit different:

```bash
neo-says tui   # Press 'f' to favorite in the TUI
```

### Filtering

Drill down by category or tag:

```bash
neo-says -c debugging          # Category filter
neo-says -t wisdom             # Tag filter
neo-says -l                    # List all categories
neo-says --list-tags           # List all tags
```

### Pipe-Friendly

Strip formatting for scripting and piping:

```bash
neo-says --raw | cowsay        # Pipe raw text anywhere
neo-says --raw >> ~/quotes.txt # Collect your favorites
```

---

## Documentation

| Section | Description |
|---------|-------------|
| [Getting Started](getting-started.md) | Installation, first run, configuration |
| [Configuration](configuration.md) | Themes, language, defaults |
| [Contributing](contributing.md) | Dev setup, adding quotes, writing themes, PR process |

---

## Why neo-says?

Because every developer deserves a CLI tool that reminds them:

- Your `TODO` comments from 2019 are not coming back.
- `git blame` has entered the chat.
- That "temporary" workaround is now load-bearing.

Built with [Rich](https://github.com/Textualize/rich) and
[Textual](https://github.com/Textualize/textual). MIT Licensed.
