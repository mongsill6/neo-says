# Themes

> "You want your wisdom to look pretty? Fine. Pick a theme. But don't blame me if the truth still hurts." -- Neo

Neo Says ships with **4 built-in themes** for rendering quotes. Each theme has its own personality -- much like Neo, except Neo's personality is better.

## Available Themes

The following themes are available out of the box:

| Theme       | Style                  | Colors           | Best For                      |
|-------------|------------------------|------------------|-------------------------------|
| `box`       | Rich panel with border | Cyan border, bold text, dim author | Terminal dashboards, daily quotes |
| `minimal`   | Clean, no borders      | Green text, dim yellow author | Piping, minimal setups        |
| `ascii-art` | ASCII frame            | Bold white text, magenta author | Retro terminals, SSH sessions |
| `cowsay`    | Speech bubble + robot  | Plain text       | Fun, screenshots, showing off |

### Theme: `box` (default)

A clean panel with a cyan border, powered by the `rich` library. Bold quote text with a dimmed author attribution.

```
╭──────────────────────────────────────────────────────╮
│ Your code doesn't need comments. It needs a          │
│ therapist.                                           │
│                                                      │
│ -- Neo                                               │
╰──────────────────────────────────────────────────────╯
```

```bash
neo-says --theme box
```

### Theme: `minimal`

No borders. No nonsense. Just green text and a dim yellow author, separated by an em-dash. For those who believe less is more (Neo disagrees, but whatever).

```
Your code doesn't need comments. It needs a therapist. — Neo
```

```bash
neo-says --theme minimal
```

### Theme: `ascii-art`

Old-school ASCII frame using `+`, `-`, and `|` characters. Quote text rendered in bold white, author in magenta. For when you want your terminal to feel like 1992.

```
+----------------------------------------------------+
| Your code doesn't need comments. It needs a        |
| therapist.                                         |
|                                                    |
|                                          -- Neo    |
+----------------------------------------------------+
```

```bash
neo-says --theme ascii-art
```

### Theme: `cowsay`

A speech bubble with Neo's signature matrix robot character. Because nothing says "I take my career seriously" like ASCII art.

```
 ______________________________________________________
/ Your code doesn't need comments. It needs a          \
\ therapist.                                -- Neo     /
 ------------------------------------------------------
        \
         \
          \
           [O_O]
           /|__|\
            |  |
           _/  \_
```

```bash
neo-says --theme cowsay
```

## Setting the Default Theme

Tired of typing `--theme` every time? Set a default and move on with your life.

### Via CLI flag

```bash
neo-says --set-theme cowsay
# Output: Default theme set to: cowsay
```

This writes to your config file at `~/.neo-says.toml`.

### Via config file

Edit `~/.neo-says.toml` directly:

```toml
[display]
theme = "cowsay"
author = "Neo"
```

### Priority order

1. `--theme` CLI argument (highest priority)
2. `display.theme` in `~/.neo-says.toml`
3. Falls back to `"box"` (the default)

## Customizing the Author

Don't want "Neo" taking credit? You can change the author name in the config:

```toml
[display]
theme = "box"
author = "The Oracle"
```

Every theme respects the `author` setting. The author appears as the attribution line in all rendered output.

## Using Themes Programmatically

You can import and use the theme system directly in Python:

```python
from neo_says.themes import render_quote, AVAILABLE_THEMES

# Print available themes
print(AVAILABLE_THEMES)
# ['box', 'minimal', 'ascii-art', 'cowsay']

# Render and print a quote with a specific theme
render_quote(
    "Debugging is just being a detective in a crime movie where you are also the murderer.",
    author="Neo",
    theme="cowsay",
)
```

### Getting the rendered string (without printing)

Each theme has its own render function that returns a string:

```python
from neo_says.themes import render_box, render_minimal, render_ascii_art, render_cowsay

# Get the rendered output as a string
output = render_box("Your code works. I'm as surprised as you are.", author="Neo")
print(type(output))  # <class 'str'>

output = render_cowsay("Sleep is just a patch for the exhaustion bug.", author="Neo")
```

| Function            | Theme       | Returns                                |
|---------------------|-------------|----------------------------------------|
| `render_box()`      | `box`       | Rich Panel string with ANSI codes      |
| `render_minimal()`  | `minimal`   | Colored text string with ANSI codes    |
| `render_ascii_art()`| `ascii-art` | ASCII frame with ANSI color codes      |
| `render_cowsay()`   | `cowsay`    | Plain-text speech bubble + robot       |

### Text wrapping

All themes automatically word-wrap text to a maximum width of **50 characters** (`MAX_WIDTH`). You don't need to worry about long quotes breaking your terminal layout. Neo handles it. Reluctantly.

## Raw Output (No Theme)

If you need plain text with zero formatting -- for piping, scripting, or because you hate fun:

```bash
# Plain text, no theme applied
neo-says --raw

# Pipe to other commands
neo-says --raw | cowsay -f tux
neo-says --raw >> ~/daily-wisdom.txt
```

## Theme + Language Combos

Themes work with all supported languages (`en`, `ko`, `ja`):

```bash
neo-says --theme ascii-art --lang ko
neo-says --theme cowsay --lang ja
```
