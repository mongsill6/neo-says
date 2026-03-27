# Plugins & Extensions

> "Oh, you want to extend me? Bold. Let's see if you can keep up." -- Neo

Neo Says is more than just a one-trick pony. It has a quote pack system, a TUI dashboard, a favorites system, and shell integration. This page covers all of it.

---

## Quote Pack System

The built-in quotes are fine. Great, even. But maybe you want quotes about Kubernetes, or your team's inside jokes, or motivational nonsense from your tech lead. That's what **quote packs** are for.

### How Packs Work

- Packs are **YAML files** containing collections of quotes
- They live in `~/.neo-says/packs/`
- Each pack has a name, version, and a list of quotes
- Packs can be installed, listed, and removed via the CLI
- When using `--pack`, quotes are selected using weighted random selection

### Pack File Format (YAML)

Here's the anatomy of a quote pack:

```yaml
name: devops-nightmares
version: "1.0"
author: "Your Name"
description: "Quotes for when the deploy goes wrong at 3am"

quotes:
  - text: "It works on my machine. Ship my machine."
    category: deployment
    tags:
      - docker
      - famous-last-words
    weight: 5

  - text: "There is no cloud. It's just someone else's computer that's also on fire."
    category: infrastructure
    tags:
      - cloud
      - reality
    weight: 3

  - text: "kubectl apply -f yolo.yaml"
    category: kubernetes
    tags:
      - k8s
      - dangerous
    weight: 2
```

#### Required Fields

| Field      | Type   | Description                          |
|------------|--------|--------------------------------------|
| `name`     | string | Unique pack identifier               |
| `version`  | string | Pack version                         |
| `quotes`   | list   | Array of quote objects               |

#### Quote Object Fields

| Field      | Type   | Required | Default | Description                    |
|------------|--------|----------|---------|--------------------------------|
| `text`     | string | Yes      | --      | The quote text                 |
| `category` | string | Yes      | --      | Category name                  |
| `tags`     | list   | No       | `[]`    | List of tag strings            |
| `weight`   | int    | No       | `3`     | Selection weight (higher = more likely) |

The `weight` field controls how often a quote gets picked. A quote with `weight: 5` is roughly 2.5x more likely to appear than one with `weight: 2`.

### Installing a Pack

```bash
# Install from a local YAML file
neo-says pack install ./my-quotes.yaml
# Output: Pack 'my-quotes' installed successfully.

# The file gets copied to ~/.neo-says/packs/
```

Only `.yaml` and `.yml` files are accepted. The pack is validated on install -- if it's missing required fields, Neo will reject it and tell you what's wrong.

### Listing Installed Packs

```bash
neo-says pack list
```

Output:

```
Installed packs (2):

  devops-nightmares    v1.0     (15 quotes)
                       Quotes for when the deploy goes wrong at 3am

  team-inside-jokes    v2.1     (8 quotes)
                       You had to be there
```

### Removing a Pack

```bash
neo-says pack remove devops-nightmares
# Output: Pack 'devops-nightmares' removed.
```

### Using Pack Quotes

```bash
# Random quote from a specific pack
neo-says --pack devops-nightmares

# Random quote from ALL installed packs
neo-says --pack all

# Combine with themes
neo-says --pack devops-nightmares --theme cowsay

# Raw output from a pack
neo-says --pack team-inside-jokes --raw
```

---

## TUI Dashboard

For the visually inclined, Neo Says includes a full **terminal UI** built with [Textual](https://textual.textualize.io/). Browse quotes, filter by category, search, toggle favorites -- all without leaving your terminal.

### Launching the TUI

```bash
neo-says tui
```

### Layout

The TUI has two panels:

- **Sidebar (left, 25%)**: Language selector, category list, favorites button
- **Main panel (right, 75%)**: Search bar and quote list

### Keyboard Shortcuts

| Key     | Action                          |
|---------|---------------------------------|
| `q`     | Quit the TUI                    |
| `f`     | Toggle favorite on highlighted quote |
| `/`     | Focus the search bar            |
| `Tab`   | Cycle focus: list -> search -> language -> list |
| `Escape`| Clear search (or unfocus search bar) |

### Features

- **Language switching**: Click a language radio button (`en`, `ko`, `ja`) to switch the entire quote database
- **Category filtering**: Click any category in the sidebar to filter quotes. Click "All" to reset
- **Search**: Type in the search bar to filter quotes by text (case-insensitive, real-time)
- **Favorites**: Click the star button in the sidebar to show only favorited quotes. Press `f` on any quote to toggle its favorite status

### Quote Display

Each quote in the list shows:

```
★  Your code doesn't need comments. It needs a therapist.
[debugging]  #truth #harsh
```

- `★` = favorited, `☆` = not favorited
- Category in brackets
- Tags prefixed with `#`

---

## Favorites System

Found a quote that speaks to your soul? Save it. Neo won't judge. (Neo will absolutely judge.)

### How Favorites Work

- Favorites are stored in `~/.neo-says-favorites.json`
- Each favorite records the text, category, tags, and timestamp
- Favorites persist across sessions and are shared between CLI and TUI

### Storage Format

```json
{
  "favorites": [
    {
      "text": "Your code doesn't need comments. It needs a therapist.",
      "category": "debugging",
      "tags": ["truth", "harsh"],
      "added_at": "2026-03-27T14:30:00.123456"
    }
  ]
}
```

### Managing Favorites via TUI

The easiest way to manage favorites is through the TUI:

1. Launch: `neo-says tui`
2. Navigate to a quote with arrow keys
3. Press `f` to toggle favorite
4. Click the `★ Favorites` button in the sidebar to view all favorites

### Using Favorites Programmatically

```python
from neo_says.favorites import (
    add_favorite,
    remove_favorite,
    is_favorite,
    load_favorites,
    search_favorites,
    get_favorites_by_category,
    clear_favorites,
)

# Add a favorite
add_favorite(
    "Sleep is just a patch for the exhaustion bug.",
    category="lifestyle",
    tags=["sleep", "bugs"],
)

# Check if favorited
is_favorite("Sleep is just a patch for the exhaustion bug.")
# True

# Search favorites
results = search_favorites("sleep")

# Filter by category
debugging_favs = get_favorites_by_category("debugging")

# Remove one
remove_favorite("Sleep is just a patch for the exhaustion bug.")

# Nuclear option: remove all
count = clear_favorites()
print(f"Removed {count} favorites. Hope you meant that.")
```

---

## Shell Integration

Make Neo a part of your daily terminal life. Because you deserve unsolicited opinions every time you open a shell.

### Bash

Add to `~/.bashrc`:

```bash
# Neo says something every time you open a terminal
neo-says

# Or the quote of the day (same quote all day)
neo-says --today

# With your favorite theme
neo-says --theme cowsay

# Only if the command exists (safe for shared dotfiles)
command -v neo-says &>/dev/null && neo-says --today --theme minimal
```

### Zsh

Add to `~/.zshrc`:

```zsh
# Random quote on shell start
neo-says --theme box

# Quote of the day with language detection
neo-says --today
```

### Fish

Add to `~/.config/fish/config.fish`:

```fish
# Neo greets you in fish
if command -v neo-says &>/dev/null
    neo-says --theme ascii-art
end
```

### MOTD (Message of the Day)

For servers, add to `/etc/profile.d/neo-says.sh`:

```bash
#!/bin/bash
if command -v neo-says &>/dev/null; then
    neo-says --today --theme box
fi
```

### Scripting with Raw Output

Use `--raw` for clean, pipeable output:

```bash
# Save quote of the day to a file
neo-says --today --raw >> ~/quotes-log.txt

# Use in a notification
neo-says --raw | notify-send "Neo Says"

# Slack webhook
curl -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"$(neo-says --raw)\"}"
```
