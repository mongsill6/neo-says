"""Tests for FastAPI server endpoints."""

import pytest
from starlette.testclient import TestClient

from neo_says.server.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


# --- Root endpoint ---


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_has_welcome_message(self, client):
        response = client.get("/")
        data = response.json()
        assert isinstance(data, dict)
        # Should contain some kind of message or welcome text
        assert any(
            key in data for key in ("message", "welcome", "name", "description")
        )


# --- GET /quote ---


class TestQuoteEndpoint:
    def test_quote_returns_200(self, client):
        response = client.get("/quote")
        assert response.status_code == 200

    def test_quote_has_required_fields(self, client):
        data = client.get("/quote").json()
        assert "text" in data
        assert "category" in data
        assert "lang" in data

    def test_quote_default_lang_is_en(self, client):
        data = client.get("/quote").json()
        assert data["lang"] == "en"

    def test_quote_text_is_nonempty_string(self, client):
        data = client.get("/quote").json()
        assert isinstance(data["text"], str)
        assert len(data["text"]) > 0

    def test_quote_with_category_filter(self, client):
        response = client.get("/quote", params={"category": "debugging"})
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "debugging"

    def test_quote_with_tag_filter(self, client):
        response = client.get("/quote", params={"tag": "humor"})
        assert response.status_code == 200
        data = response.json()
        assert "text" in data

    def test_quote_lang_ko(self, client):
        response = client.get("/quote", params={"lang": "ko"})
        assert response.status_code == 200
        data = response.json()
        assert data["lang"] == "ko"

    def test_quote_lang_ja(self, client):
        response = client.get("/quote", params={"lang": "ja"})
        assert response.status_code == 200
        data = response.json()
        assert data["lang"] == "ja"

    def test_quote_with_category_and_lang(self, client):
        response = client.get("/quote", params={"category": "debugging", "lang": "ko"})
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "debugging"
        assert data["lang"] == "ko"


# --- GET /quote/today ---


class TestQuoteOfTheDay:
    def test_today_returns_200(self, client):
        response = client.get("/quote/today")
        assert response.status_code == 200

    def test_today_has_required_fields(self, client):
        data = client.get("/quote/today").json()
        assert "text" in data
        assert "category" in data
        assert "lang" in data

    def test_today_is_consistent(self, client):
        """Quote of the day should return the same quote on repeated calls."""
        first = client.get("/quote/today").json()
        second = client.get("/quote/today").json()
        assert first["text"] == second["text"]
        assert first["category"] == second["category"]

    def test_today_with_lang_ko(self, client):
        response = client.get("/quote/today", params={"lang": "ko"})
        assert response.status_code == 200
        assert response.json()["lang"] == "ko"

    def test_today_with_lang_ja(self, client):
        response = client.get("/quote/today", params={"lang": "ja"})
        assert response.status_code == 200
        assert response.json()["lang"] == "ja"


# --- GET /quote/{category} ---


class TestQuoteByCategory:
    @pytest.mark.parametrize(
        "category",
        ["debugging", "code-review", "git", "production", "meetings", "general"],
    )
    def test_valid_categories_return_200(self, client, category):
        response = client.get(f"/quote/{category}")
        assert response.status_code == 200

    def test_category_matches_path(self, client):
        data = client.get("/quote/debugging").json()
        assert data["category"] == "debugging"

    def test_category_with_lang_param(self, client):
        response = client.get("/quote/debugging", params={"lang": "ko"})
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "debugging"
        assert data["lang"] == "ko"

    def test_invalid_category_returns_404(self, client):
        response = client.get("/quote/nonexistent-category-xyz")
        assert response.status_code == 404

    def test_invalid_category_error_body(self, client):
        response = client.get("/quote/nonexistent-category-xyz")
        data = response.json()
        assert "detail" in data or "error" in data


# --- GET /categories ---


class TestCategoriesEndpoint:
    def test_categories_returns_200(self, client):
        response = client.get("/categories")
        assert response.status_code == 200

    def test_categories_returns_list(self, client):
        data = client.get("/categories").json()
        assert isinstance(data["categories"], list)

    def test_categories_is_nonempty(self, client):
        data = client.get("/categories").json()
        assert len(data["categories"]) > 0

    def test_known_categories_present(self, client):
        cats = client.get("/categories").json()["categories"]
        assert "debugging" in cats
        assert "code-review" in cats

    def test_categories_are_sorted(self, client):
        cats = client.get("/categories").json()["categories"]
        assert cats == sorted(cats)


# --- GET /tags ---


class TestTagsEndpoint:
    def test_tags_returns_200(self, client):
        response = client.get("/tags")
        assert response.status_code == 200

    def test_tags_returns_list(self, client):
        data = client.get("/tags").json()
        assert isinstance(data["tags"], list)

    def test_tags_is_nonempty(self, client):
        data = client.get("/tags").json()
        assert len(data["tags"]) > 0

    def test_known_tags_present(self, client):
        tags = client.get("/tags").json()["tags"]
        assert "humor" in tags
        assert "sarcasm" in tags

    def test_tags_are_sorted(self, client):
        tags = client.get("/tags").json()["tags"]
        assert tags == sorted(tags)


# --- GET /health ---


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_ok(self, client):
        data = client.get("/health").json()
        assert data["status"] == "ok"


# --- Edge cases and content type ---


class TestEdgeCases:
    def test_responses_are_json(self, client):
        for path in ["/", "/quote", "/quote/today", "/categories", "/tags", "/health"]:
            response = client.get(path)
            assert "application/json" in response.headers.get("content-type", "")

    def test_quote_lang_defaults_without_param(self, client):
        """When no lang param is given, default to English."""
        data = client.get("/quote").json()
        assert data["lang"] == "en"

    def test_unsupported_endpoint_returns_404(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404
