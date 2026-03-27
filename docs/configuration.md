# Configuration

Neo remembers your preferences so you don't have to repeat yourself. How thoughtful.

## Config File

All configuration lives in a single TOML file:

```
~/.neo-says.toml
```

Here is the full schema with all available options:

```toml
[display]
theme = "box"       # Display theme: "box", "minimal", "ascii-art", "cowsay"
author = "Neo"      # Attribution name shown below quotes

[locale]
lang = "auto"       # Language: "auto", "en", "ko", "ja"
```

## Options Reference

### `[display]` section

#### `theme`

Controls how quotes are visually rendered in the terminal.

| Value        | Description                                         |
|:-------------|:----------------------------------------------------|
| `"box"`      | Rich panel with cyan border (default)               |
| `"minimal"`  | Colored text with no borders                        |
| `"ascii-art"`| Classic ASCII frame using `+`, `-`, `\|` characters |
| `"cowsay"`   | Speech bubble with Neo's robot avatar               |

```toml
[display]
theme = "minimal"
```

!!! tip "Try them all"
    Run `neo-says --theme <name>` to preview a theme without changing your config. When you find the one you like:

    ```bash
    neo-says --set-theme minimal
    ```

#### `author`

The name displayed in the attribution line below each quote. Defaults to `"Neo"`.

```toml
[display]
author = "The Matrix"
```

This changes the `-- Neo` line to `-- The Matrix` (or whatever you set).

!!! note
    There is no CLI flag for `--set-author`. Edit `~/.neo-says.toml` directly to change this.

### `[locale]` section

#### `lang`

Controls the language of the quote database.

| Value    | Description                                          |
|:---------|:-----------------------------------------------------|
| `"auto"` | Detect from system `LANG` env var (default)          |
| `"en"`   | English                                              |
| `"ko"`   | Korean                                               |
| `"ja"`   | Japanese                                             |

```toml
[locale]
lang = "ko"
```

When set to `"auto"`, the detection follows this logic:

1. Check system `LANG` environment variable (e.g., `ko_KR.UTF-8` resolves to `ko`)
2. If no match found, fall back to `"en"`

## Environment Variables

### `LANG`

The standard system locale variable. When `locale.lang` is set to `"auto"` (the default), Neo reads this to determine the quote language.

```bash
# This will serve Korean quotes (if lang is "auto")
export LANG=ko_KR.UTF-8
neo-says
```

Only the first two characters (the language code) are extracted. If the detected code is not one of the supported languages (`en`, `ko`, `ja`), Neo falls back to English.

## Config Precedence

When multiple sources define the same setting, this is the priority order (highest wins):

```
CLI arguments  >  Config file (~/.neo-says.toml)  >  Environment variables  >  Defaults
```

Concretely for language detection:

| Priority | Source                   | Example                          |
|---------:|:-------------------------|:---------------------------------|
| 1        | `--lang` CLI argument    | `neo-says --lang ja`             |
| 2        | Config file `locale.lang`| `lang = "ko"` in config          |
| 3        | `LANG` env var           | `LANG=ko_KR.UTF-8`              |
| 4        | Default                  | `"en"`                           |

For theme selection:

| Priority | Source                    | Example                          |
|---------:|:--------------------------|:---------------------------------|
| 1        | `--theme` CLI argument    | `neo-says --theme cowsay`        |
| 2        | Config file `display.theme`| `theme = "minimal"` in config   |
| 3        | Default                   | `"box"`                          |

## Setting Config via CLI

You can modify the config file without opening an editor:

```bash
# Set default theme
neo-says --set-theme cowsay

# Set default language
neo-says --set-lang ja
```

These commands write directly to `~/.neo-says.toml`. If the file doesn't exist, it will be created.

!!! warning
    The `--set-theme` and `--set-lang` commands modify the file and exit immediately. They do not display a quote.

## Example Configurations

### The Minimalist

You like things clean. No borders, English only.

```toml
[display]
theme = "minimal"
author = "Neo"

[locale]
lang = "en"
```

### The Retro Dev

ASCII art, custom attribution, system locale detection.

```toml
[display]
theme = "ascii-art"
author = "The Oracle"

[locale]
lang = "auto"
```

### The Multilingual Team Lead

Japanese quotes with the cowsay theme. Because why not.

```toml
[display]
theme = "cowsay"
author = "Sensei"

[locale]
lang = "ja"
```

### Shell Startup Integration

Add Neo to your shell profile for daily wisdom:

```bash
# In ~/.bashrc or ~/.zshrc
if command -v neo-says &> /dev/null; then
    neo-says --today
fi
```

Pair this with a config file and you get personalized quotes every time you open a terminal. You're welcome.

## Config File Location

The config file is always at `~/.neo-says.toml` (i.e., `$HOME/.neo-says.toml`). This path is not configurable.

If the file does not exist, Neo uses these defaults silently:

```toml
[display]
theme = "box"
author = "Neo"

[locale]
lang = "auto"
```

No errors, no warnings. Neo just works.
