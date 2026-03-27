# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-03-27

### Added

#### Phase 1 — Initial Release: Core CLI & Quote Engine
- Initial project scaffold as a single-file snarky CLI fortune teller for developers
- `src/` layout with `pyproject.toml`, setuptools build backend, and `neo-says` entry point
- JSON-based quote database (`data/quotes.json`) with 150+ developer quotes
- Quote fields: `text`, `category`, `tags` (list), `weight` (float for biased random selection)
- Categories: `git`, `debugging`, `meetings`, `code-review`, `production`, `general`
- Weighted random quote selection — quotes with higher weight surface more frequently
- Deterministic quote-of-the-day via `--today` flag (same quote for entire UTC day)
- Category filter: `-c <category>` / `--category <category>`
- Tag filter: `-t <tag>` / `--tag <tag>`
- Raw output mode: `--raw` for piping into scripts, clipboard managers, or notifications
- `--list-categories` and `--list-tags` flags
- `rich` library integration for styled terminal output

#### Phase 2 — Theme System
- Four built-in display themes: `box`, `minimal`, `ascii-art`, `cowsay`
  - `box` — rich-rendered cyan-bordered panel (default)
  - `minimal` — plain colored text with no borders
  - `ascii-art` — retro `+---+` frame with ANSI color escape codes
  - `cowsay` — speech bubble with Neo's ASCII robot character art
- `--theme <name>` flag for per-run theme selection
- `--set-theme <name>` to persist default theme to `~/.neo-says.toml`
- `--set-author <name>` to customize the attribution footer
- Config file support (`~/.neo-says.toml`) with `[display]` and `[locale]` sections
- `src/neo_says/themes.py` module encapsulating all rendering logic
- `src/neo_says/config.py` module for TOML config load/save

#### Phase 3 — Internationalization (i18n)
- Korean quote database (`data/quotes_ko.json`) with 30+ developer quotes
- Japanese quote database (`data/quotes_ja.json`) with 20+ developer quotes
- `--lang <code>` flag supporting `en`, `ko`, `ja`
- `--set-lang <code>` for persistent language preference
- Automatic language detection from `LANG` / `LANGUAGE` environment variables
- Locale-aware category and tag filtering (each language maintains its own category set)
- `SUPPORTED_LANGS` constant exported from `src/neo_says/quotes.py`

#### Phase 4 — Interactive TUI Browser
- Full-screen terminal UI built with [Textual](https://textual.textualize.io/) (`neo-says tui`)
- Three-panel layout: sidebar (filters), quote list, detail pane
- Sidebar controls: language selector, category filter dropdown, favorites-only toggle
- Real-time full-text search with `/` keybinding
- Favorites system: `f` to toggle, persisted to `~/.neo-says-favorites.json`
- Keyboard shortcuts: `↑↓` navigate, `Tab` cycle panels, `Esc` clear search, `q` quit
- `src/neo_says/tui.py` Textual app and `src/neo_says/favorites.py` persistence module

#### Phase 5 — YAML Plugin / Pack System
- YAML-based quote pack format with `name`, `version`, `author`, `description`, `quotes` fields
- Pack install/list/remove subcommands: `neo-says pack install <file>`, `pack list`, `pack remove <name>`
- Packs installed to `~/.neo-says/packs/`
- Schema validation on install — rejects malformed packs with descriptive errors
- `--pack <name>` to draw exclusively from a named pack; `--pack all` to merge all packs with built-ins
- Three sample packs in `sample-packs/`: `crypto-bro.yaml`, `devops-wisdom.yaml`, `startup-life.yaml`
- `src/neo_says/packs.py` module for pack loading, validation, and registry management

#### Phase 6 & 7 — FastAPI REST API + Docker
- Optional `[server]` extras: `fastapi`, `uvicorn[standard]`, `slowapi`
- FastAPI application at `src/neo_says/server/app.py` with Pydantic response models
- API endpoints:
  - `GET /` — welcome message with endpoint index
  - `GET /quote` — random quote (`?category=`, `?tag=`, `?lang=`)
  - `GET /quote/today` — deterministic quote of the day (`?lang=`)
  - `GET /quote/{category}` — random quote from a specific category (`?lang=`)
  - `GET /categories` — list all categories (`?lang=`)
  - `GET /tags` — list all tags (`?lang=`)
  - `GET /health` — health check
- SlowAPI rate limiting: 15 requests/minute per IP
- CORS middleware enabled (all origins)
- OpenAPI / Swagger UI at `/docs`, ReDoc at `/redoc`
- `python -m neo_says.server` entry point
- `Dockerfile` (Python 3.11 slim, non-root user)
- `docker-compose.yml` with port `8000` mapping and restart policy

#### Phase 8 — Shell Integration
- Bash completion script: `completions/neo-says.bash`
- Zsh completion script: `completions/_neo-says`
- Fish completion script: `completions/neo-says.fish`
- `install.sh` — detects shell, installs completions, optionally sets up MOTD
  - `--with-motd` flag appends `neo-says` invocation to shell profile for login quotes
- Homebrew formula: `Formula/neo-says.rb`
- `scripts/` directory for auxiliary tooling

#### Phase 9 — CI/CD (GitHub Actions)
- `ci.yml` — lint + test matrix across Python 3.9, 3.10, 3.11, 3.12 on push and PR
- `docs.yml` — MkDocs build and GitHub Pages deploy on push to `main`
- `publish.yml` — PyPI release workflow triggered on version tag (`v*`)
- Ruff linting and formatting checks in CI
- mypy static type checking in CI
- `.pre-commit-config.yaml` with ruff, black, and mypy hooks
- `tests/` directory with pytest suite

#### Phase 10 — MkDocs Documentation Site
- `mkdocs.yml` configuration using MkDocs Material theme
- Documentation pages:
  - `docs/index.md` — project overview and quick start
  - `docs/getting-started.md` — installation and first use
  - `docs/configuration.md` — config file reference
  - `docs/themes.md` — theme gallery and customization
  - `docs/plugins.md` — pack system guide and YAML schema
  - `docs/api-reference.md` — REST API endpoint reference
  - `docs/contributing.md` — contribution workflow
- `docs/stylesheets/` — custom CSS overrides
- Deployed to https://mongsill6.github.io/neo-says via GitHub Actions

#### Phase 11 — Community
- `CONTRIBUTING.md` — development setup, coding standards, PR checklist, commit message conventions (Conventional Commits)
- `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1
- GitHub issue templates:
  - Bug report template (`bug-report.yml`)
  - Quote submission template (`quote-submission.yml`) — no code required
- Pull request template

---

## [1.0.0] - 2026-03-27

### Added

- Initial single-file proof of concept: `neo_says.py`
- Hardcoded quote list with `git`, `debugging`, `meetings`, `code-review`, `production`, `general` categories
- `--category` CLI flag
- Basic `rich` panel output with cyan border
- MIT license

[2.0.0]: https://github.com/mongsill6/neo-says/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/mongsill6/neo-says/releases/tag/v1.0.0
