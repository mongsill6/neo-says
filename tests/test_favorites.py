import pytest
from neo_says.favorites import (
    load_favorites,
    save_favorites,
    add_favorite,
    remove_favorite,
    is_favorite,
    get_favorites_by_category,
    search_favorites,
    clear_favorites,
)


@pytest.fixture
def fake_favorites_path(tmp_path, monkeypatch):
    path = tmp_path / "test-favorites.json"
    monkeypatch.setattr("neo_says.favorites.get_favorites_path", lambda: path)
    return path


def test_load_favorites_empty(fake_favorites_path):
    result = load_favorites()
    assert result == []


def test_add_favorite(fake_favorites_path):
    result = add_favorite("Hello world", "greetings", ["hello", "world"])
    assert result is True
    favorites = load_favorites()
    assert len(favorites) == 1
    assert favorites[0]["text"] == "Hello world"
    assert favorites[0]["category"] == "greetings"
    assert favorites[0]["tags"] == ["hello", "world"]


def test_add_favorite_duplicate(fake_favorites_path):
    add_favorite("Duplicate text", "misc")
    result = add_favorite("Duplicate text", "other")
    assert result is False
    favorites = load_favorites()
    assert len(favorites) == 1


def test_remove_favorite(fake_favorites_path):
    add_favorite("Remove me", "test")
    result = remove_favorite("Remove me")
    assert result is True
    favorites = load_favorites()
    assert len(favorites) == 0


def test_remove_favorite_not_found(fake_favorites_path):
    result = remove_favorite("Does not exist")
    assert result is False


def test_is_favorite(fake_favorites_path):
    add_favorite("I exist", "test")
    assert is_favorite("I exist") is True
    assert is_favorite("I do not exist") is False


def test_get_favorites_by_category(fake_favorites_path):
    add_favorite("Item A", "alpha")
    add_favorite("Item B", "beta")
    add_favorite("Item C", "alpha")

    alpha_favorites = get_favorites_by_category("alpha")
    assert len(alpha_favorites) == 2
    assert all(f["category"] == "alpha" for f in alpha_favorites)

    beta_favorites = get_favorites_by_category("beta")
    assert len(beta_favorites) == 1
    assert beta_favorites[0]["text"] == "Item B"

    empty = get_favorites_by_category("gamma")
    assert empty == []


def test_search_favorites(fake_favorites_path):
    add_favorite("Hello World", "greetings")
    add_favorite("Goodbye World", "farewells")
    add_favorite("Something else", "misc")

    results = search_favorites("world")
    assert len(results) == 2

    results_upper = search_favorites("HELLO")
    assert len(results_upper) == 1
    assert results_upper[0]["text"] == "Hello World"

    no_results = search_favorites("xyz_not_found")
    assert no_results == []


def test_clear_favorites(fake_favorites_path):
    add_favorite("One", "test")
    add_favorite("Two", "test")
    add_favorite("Three", "test")

    count = clear_favorites()
    assert count == 3

    favorites = load_favorites()
    assert favorites == []


def test_add_favorite_stores_timestamp(fake_favorites_path):
    add_favorite("Timestamped entry", "test")
    favorites = load_favorites()
    assert len(favorites) == 1
    assert "added_at" in favorites[0]
    assert favorites[0]["added_at"] is not None
