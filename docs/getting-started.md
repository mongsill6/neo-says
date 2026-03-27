# Getting Started

So you want snarky developer wisdom piped directly into your terminal? Good choice. Let Neo enlighten you.

## Installation

=== "pip (recommended)"

    ```bash
    pip install neo-says
    ```

=== "From source"

    ```bash
    git clone https://github.com/mongsill6/neo-says.git
    cd neo-says
    pip install .
    ```

=== "Development mode"

    ```bash
    git clone https://github.com/mongsill6/neo-says.git
    cd neo-says
    pip install -e ".[dev]"
    ```

!!! tip "Want the REST API server too?"
    Install with the server extras:

    ```bash
    pip install "neo-says[server]"
    ```

### Requirements

- Python 3.8 or later
- A terminal that can handle the truth

## Quick Start

### Get a random quote

Just run it. No arguments needed. Neo will decide what wisdom you deserve today.

```bash
neo-says
```

```
╭──────────────────────────────────────────────────────╮
│ The code works on my machine. Ship the machine.      │
│                                                      │
│ -- Neo                                               │
╰──────────────────────────────────────────────────────╯
```

### Pick a theme

Neo comes with four visual themes. Because even cynicism deserves good presentation.

=== "box (default)"

    ```bash
    neo-says --theme box
    ```

    A clean bordered panel with cyan edges. Classy.

=== "minimal"

    ```bash
    neo-says --theme minimal
    ```

    Just colored text. No borders. For the minimalists among us.

=== "ascii-art"

    ```bash
    neo-says --theme ascii-art
    ```

    Old-school ASCII frame. `+---+` and all that retro goodness.

=== "cowsay"

    ```bash
    neo-says --theme cowsay
    ```

    A speech bubble with Neo's robot avatar. Yes, seriously.

### Filter by category

```bash
# List all available categories
neo-says --list-categories

# Get a quote from a specific category
neo-says -c debugging
```

### Filter by tag

```bash
# List all available tags
neo-says --list-tags

# Get a quote with a specific tag
neo-says -t hacker
```

### Quote of the day

Get a deterministic daily quote -- the same one all day, different tomorrow.

```bash
neo-says --today
```

### Switch languages

Neo speaks multiple languages. Currently supported: English (`en`), Korean (`ko`), and Japanese (`ja`).

```bash
# Quotes in Korean
neo-says --lang ko

# Quotes in Japanese
neo-says --lang ja
```

!!! info "Language auto-detection"
    If you don't pass `--lang`, Neo checks your config file, then your system `LANG` environment variable, and falls back to English. Smart, right?

### Raw output (for piping)

Strip all the fancy formatting and get plain text -- useful for piping into other commands.

```bash
# Pipe a quote into your clipboard
neo-says --raw | xclip -selection clipboard

# Use in a script
QUOTE=$(neo-says --raw)
echo "Today's wisdom: $QUOTE"
```

### Interactive TUI

Browse quotes interactively with a full terminal UI powered by Textual.

```bash
neo-says tui
```

### Quote packs

Install custom quote packs from YAML files for even more wisdom (or nonsense).

```bash
# Install a pack
neo-says pack install my-quotes.yaml

# List installed packs
neo-says pack list

# Use quotes from a specific pack
neo-says --pack my-quotes

# Use quotes from ALL installed packs
neo-says --pack all

# Remove a pack
neo-says pack remove my-quotes
```

## Your First Config File

Tired of typing `--theme cowsay --lang ko` every time? Create a config file.

```bash
# Set your default theme (saves to ~/.neo-says.toml)
neo-says --set-theme cowsay

# Set your default language
neo-says --set-lang ko
```

Or create `~/.neo-says.toml` by hand:

```toml
[display]
theme = "cowsay"
author = "Neo"

[locale]
lang = "ko"
```

!!! note
    CLI arguments always override the config file. So `neo-says --theme box` will use `box` even if your config says `cowsay`. See the [Configuration](configuration.md) page for the full reference.

## What's Next?

- **[Configuration](configuration.md)** -- Full config file reference, environment variables, and advanced setup
- Browse the `sample-packs/` directory for example quote pack files
- Run `neo-says --help` for the complete CLI reference

Now go forth and let Neo judge your code.
