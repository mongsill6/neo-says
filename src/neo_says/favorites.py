import json
import datetime
from pathlib import Path


def get_favorites_path() -> Path:
    """Returns the favorites file path."""
    return Path.home() / ".neo-says-favorites.json"


def load_favorites() -> list[dict]:
    """Load favorites from JSON file, return empty list if file doesn't exist."""
    path = get_favorites_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("favorites", [])


def save_favorites(favorites: list[dict]) -> None:
    """Save favorites list to JSON file."""
    path = get_favorites_path()
    with path.open("w", encoding="utf-8") as f:
        json.dump({"favorites": favorites}, f, ensure_ascii=False, indent=2)


def add_favorite(text: str, category: str, tags: list[str] | None = None) -> bool:
    """Add a quote to favorites, return False if already exists."""
    favorites = load_favorites()
    if any(entry["text"] == text for entry in favorites):
        return False
    favorites.append({
        "text": text,
        "category": category,
        "tags": tags or [],
        "added_at": datetime.datetime.now().isoformat(),
    })
    save_favorites(favorites)
    return True


def remove_favorite(text: str) -> bool:
    """Remove a favorite by text, return True if found and removed."""
    favorites = load_favorites()
    new_favorites = [entry for entry in favorites if entry["text"] != text]
    if len(new_favorites) == len(favorites):
        return False
    save_favorites(new_favorites)
    return True


def is_favorite(text: str) -> bool:
    """Check if a quote is already favorited."""
    return any(entry["text"] == text for entry in load_favorites())


def get_favorites_by_category(category: str) -> list[dict]:
    """Filter favorites by category."""
    return [entry for entry in load_favorites() if entry["category"] == category]


def search_favorites(query: str) -> list[dict]:
    """Search favorites by text substring (case-insensitive)."""
    lower_query = query.lower()
    return [entry for entry in load_favorites() if lower_query in entry["text"].lower()]


def clear_favorites() -> int:
    """Remove all favorites, return count of removed items."""
    favorites = load_favorites()
    count = len(favorites)
    save_favorites([])
    return count
