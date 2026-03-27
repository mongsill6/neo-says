# neo-says

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/mongsill6/neo-says/actions/workflows/ci.yml/badge.svg)](https://github.com/mongsill6/neo-says/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/neo-says)](https://pypi.org/project/neo-says/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> A snarky CLI fortune teller for developers. Because you needed more sass in your terminal.

```
    _   __                ____
   / | / /__  ____       / __/___ ___  _______
  /  |/ / _ \/ __ \     / /_/ __ `/ / / / ___/
 / /|  /  __/ /_/ /    _\ \/ /_/ / /_/ (__  )
/_/ |_/\___/\____/    /___/\__,_/\__, /____/
                                /____/

  The snarky CLI companion you didn't ask for.
```

```
$ neo-says
╭──────────────────────────────────────────────────────╮
│ "It works on my machine" is not a deployment         │
│ strategy.                                            │
│                                                      │
│ -- Neo                                               │
╰──────────────────────────────────────────────────────╯

$ neo-says --theme cowsay
 _____________________________________________
/ Your code doesn't need comments.           \
| It needs a therapist.                      |
|                                            |
\ -- Neo                                     /
 ---------------------------------------------
        \
         \
          \
           [O_O]
           /|__|\
            |  |
           _/  \_

$ neo-says --theme minimal
Debugging is twice as hard as writing the code in the
first place. — Neo

$ neo-says --lang ko
╭──────────────────────────────────────────────────────╮
│ 코드 리뷰는 당신의 코드가 아니라 당신의 자아를       │
│ 검토하는 것입니다.                                   │
│                                                      │
│ -- Neo                                               │
╰──────────────────────────────────────────────────────╯
```

---

## Features

### Phase 1 — Core Quote Engine
- JSON-based quote database with **150+ developer quotes**, categories, tags, and per-quote weights
- Weighted random selection — higher weight quotes appear more often
- Deterministic **quote of the day** based on current date (same quote all day, different tomorrow)
- Filter by category (`-c debugging`) or tag (`-t hacker`)
- Raw output mode (`--raw`) for piping into scripts, clipboard, or notifications

### Phase 2 — Theme System
- **4 built-in themes**: `box` (default), `minimal`, `ascii-art`, `cowsay`
- `box` — rich-rendered cyan-bordered panel
- `minimal` — plain colored text, no borders
- `ascii-art` — retro `+---+` ASCII frame with ANSI colors
- `cowsay` — speech bubble with Neo's ASCII robot character
- Persistent default theme via `--set-theme` saved to `~/.neo-says.toml`

### Phase 3 — Internationalization (i18n)
- Supported languages: **English** (`en`), **Korean** (`ko`, 30+ quotes), **Japanese** (`ja`, 20+ quotes)
- Language auto-detection from `LANG` environment variable
- Override per-run with `--lang ko` or set permanently with `--set-lang ko`

### Phase 4 — Interactive TUI Browser
- Full terminal UI built with [Textual](https://textual.textualize.io/)
- Sidebar with language selector, category filter, and favorites toggle
- Real-time search across all quote text
- Keyboard shortcuts: `q` quit, `f` toggle favorite, `/` search, `Tab` cycle panels, `Esc` clear
- Favorites system backed by `~/.neo-says-favorites.json`

### Phase 5 — YAML Plugin / Pack System
- YAML-based custom quote packs installed to `~/.neo-says/packs/`
- Pack commands: `pack install`, `pack list`, `pack remove`
- `--pack <name>` or `--pack all` to draw from installed packs
- Pack validation on install — invalid files are rejected with clear error messages
- **Sample packs** included: `crypto-bro`, `devops-wisdom`, `startup-life`

### Phase 6 & 7 — FastAPI REST API + Docker
- FastAPI server with interactive Swagger docs at `/docs`
- Endpoints: `GET /quote`, `GET /quote/today`, `GET /quote/{category}`, `GET /categories`, `GET /tags`, `GET /health`
- Rate limited to **15 req/min** per IP via slowapi
- Official `Dockerfile` and `docker-compose.yml` — one-command startup: `docker compose up`

### Phase 8 — Shell Integration
- Tab completion for **bash**, **zsh**, and **fish** (installed to `completions/`)
- **Homebrew formula** in `Formula/` for macOS users
- One-line installer script: `curl -fsSL .../install.sh | bash`
- MOTD support: `install.sh --with-motd`

### Phase 9 — CI/CD (GitHub Actions)
- Workflows: `ci.yml` (test matrix Python 3.9–3.12), `docs.yml` (MkDocs deploy), `publish.yml` (PyPI release)
- Linting with Ruff + mypy type checking, pre-commit hooks
- Issue templates: bug report, quote submission

### Phase 10 — MkDocs Documentation Site
- MkDocs Material theme site at https://mongsill6.github.io/neo-says
- Sections: Getting Started, Configuration, Themes, Plugins & Packs, API Reference, Contributing

### Phase 11 — Community
- `CONTRIBUTING.md` with development guide and commit conventions
- `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1)
- Issue/PR templates for structured contributions

---

## Quick Start

**pip (recommended)**

```bash
pip install neo-says
```

**One-line installer**

```bash
curl -fsSL https://raw.githubusercontent.com/mongsill6/neo-says/main/install.sh | bash
```

**With MOTD setup (shows a quote on every login)**

```bash
curl -fsSL https://raw.githubusercontent.com/mongsill6/neo-says/main/install.sh | bash -s -- --with-motd
```

**From source**

```bash
git clone https://github.com/mongsill6/neo-says.git
cd neo-says
pip install .
```

**With API server extras**

```bash
pip install "neo-says[server]"
```

**Development mode**

```bash
git clone https://github.com/mongsill6/neo-says.git
cd neo-says
pip install -e ".[dev]"
```

**Requirements:** Python 3.8 or later.

---

## Usage

```bash
# Random quote (default theme)
neo-says

# Quote of the day — deterministic, same all day
neo-says --today

# Filter by category
neo-says -c debugging
neo-says -c git
neo-says -c meetings

# Filter by tag
neo-says -t hacker
neo-says -t truth

# List available categories and tags
neo-says --list-categories
neo-says --list-tags

# Choose a display theme
neo-says --theme box
neo-says --theme minimal
neo-says --theme ascii-art
neo-says --theme cowsay

# Switch language
neo-says --lang ko
neo-says --lang ja

# Raw output for piping
neo-says --raw
neo-says --raw | xclip -selection clipboard
neo-says --today --raw >> ~/quotes-log.txt

# Send to Slack
curl -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"$(neo-says --raw)\"}"

# Launch interactive TUI
neo-says tui
```

---

## Configuration

Preferences are saved to `~/.neo-says.toml`.

**Set defaults via CLI**

```bash
neo-says --set-theme cowsay
neo-says --set-lang ko
```

**Or edit the config file directly**

```toml
[display]
theme = "cowsay"
author = "Neo"

[locale]
lang = "ko"
```

Config keys:

- `display.theme` — one of `box`, `minimal`, `ascii-art`, `cowsay`
- `display.author` — attribution name shown in the quote footer
- `locale.lang` — one of `en`, `ko`, `ja`, or `auto` (system detection)

CLI arguments always take precedence over the config file.

---

## Shell Integration

Add to `~/.bashrc` or `~/.zshrc` for a quote on every new terminal:

```bash
command -v neo-says &>/dev/null && neo-says --today --theme minimal
```

**Fish** — add to `~/.config/fish/config.fish`:

```fish
if command -v neo-says &>/dev/null
    neo-says --theme ascii-art
end
```

**Tab completion**

```bash
# Bash
source completions/neo-says.bash

# Zsh
fpath=(completions $fpath)

# Fish
cp completions/neo-says.fish ~/.config/fish/completions/
```

---

## Plugin / Pack System

Quote packs are YAML files you install into `~/.neo-says/packs/`. Each pack bundles its own quotes with metadata.

**Pack file format**

```yaml
name: devops-wisdom
version: "1.0"
author: "Your Name"
description: "Quotes for when the deploy goes wrong at 3am"

quotes:
  - text: "There is no cloud. It's just someone else's computer that's also on fire."
    category: infrastructure
    tags:
      - cloud
      - reality
    weight: 5

  - text: "kubectl apply -f yolo.yaml"
    category: kubernetes
    tags:
      - k8s
      - dangerous
    weight: 2
```

Pack fields:

- `name` — unique identifier (required)
- `version` — pack version string (required)
- `author` — pack author (optional)
- `description` — short description (optional)
- `quotes` — list of quote objects (required)

Quote object fields:

- `text` — the quote text (required)
- `category` — category name (required)
- `tags` — list of tag strings, default `[]` (optional)
- `weight` — selection weight 1–5, default `3` (optional). A quote with `weight: 5` is 2.5x more likely to appear than one with `weight: 2`.

**Managing packs**

```bash
# Install from a local file
neo-says pack install ./my-quotes.yaml

# List all installed packs
neo-says pack list

# Use quotes from a specific pack
neo-says --pack devops-wisdom

# Use quotes from all installed packs
neo-says --pack all

# Combine with themes
neo-says --pack devops-wisdom --theme cowsay

# Remove a pack
neo-says pack remove devops-wisdom
```

See the `sample-packs/` directory for ready-to-install examples: `crypto-bro.yaml`, `devops-wisdom.yaml`, and `startup-life.yaml`.

---

## API Server

The optional REST API exposes the full quote engine over HTTP.

**Start with Docker Compose**

```bash
docker compose up
```

**Or run directly**

```bash
pip install "neo-says[server]"
python -m neo_says.server
```

The server starts on `http://localhost:8000`. Interactive Swagger docs are at `/docs`.

**Endpoints**

- `GET /quote` — random quote, optional `?category=`, `?tag=`, `?lang=`
- `GET /quote/today` — quote of the day, optional `?lang=`
- `GET /quote/{category}` — random quote from a category, optional `?lang=`
- `GET /categories` — list all categories, optional `?lang=`
- `GET /tags` — list all tags, optional `?lang=`
- `GET /health` — health check

**Example requests**

```bash
# Random quote
curl http://localhost:8000/quote

# Quote of the day in Korean
curl "http://localhost:8000/quote/today?lang=ko"

# All debugging quotes
curl http://localhost:8000/quote/debugging

# List categories
curl http://localhost:8000/categories
```

All endpoints are rate limited to 15 requests per minute per IP.

---

## Contributing

Got a snarky dev quote? Found a bug? Want to add a feature?

- **Submit a quote** — open an issue using the [Quote Submission](../../issues/new?template=quote-submission.yml) template. No code required.
- **Add a quote via PR** — fork, add to `data/quotes.json`, and open a pull request. Follow the [Contributing Guide](CONTRIBUTING.md).
- **Bug reports** — use the [Bug Report](../../issues/new?template=bug-report.yml) template.
- **Code contributions** — install with `pip install -e ".[dev]"`, run `pytest`, and check the [Contributing Guide](CONTRIBUTING.md) for code style and PR rules.

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `test:`, `chore:`.

---

## License

[MIT](LICENSE) — do whatever you want, just don't sue us.
