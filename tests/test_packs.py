"""Comprehensive tests for the neo-says pack system."""

import pytest
import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def packs_dir(tmp_path, monkeypatch):
    """Redirect PACKS_DIR to a temporary directory for every test."""
    d = tmp_path / "packs"
    d.mkdir()
    monkeypatch.setattr("neo_says.packs.PACKS_DIR", d)
    return d


def _write_pack_yaml(path: Path, data: dict) -> Path:
    """Helper: dump *data* as YAML to *path* and return the path."""
    path.write_text(yaml.dump(data, default_flow_style=False), encoding="utf-8")
    return path


def _valid_pack_data(**overrides) -> dict:
    """Return a minimal valid pack dict, with optional overrides."""
    base = {
        "name": "test-pack",
        "version": "1.0",
        "author": "Tester",
        "description": "Test pack",
        "quotes": [
            {
                "text": "Test quote",
                "category": "test",
                "tags": ["humor"],
                "weight": 3,
            }
        ],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# validate_pack
# ---------------------------------------------------------------------------

class TestValidatePack:

    def test_validate_pack_valid(self):
        """A fully valid pack dict should produce zero errors."""
        from neo_says.packs import validate_pack

        errors = validate_pack(_valid_pack_data())
        assert errors == []

    def test_validate_pack_missing_fields(self):
        """Omitting required top-level fields should report each one."""
        from neo_says.packs import validate_pack

        data = {}  # missing everything
        errors = validate_pack(data)

        assert isinstance(errors, list)
        assert len(errors) > 0
        # At minimum "name" and "quotes" should be flagged
        combined = " ".join(errors).lower()
        assert "name" in combined
        assert "quotes" in combined

    def test_validate_pack_invalid_quotes_not_a_list(self):
        """If 'quotes' is not a list, validation must flag it."""
        from neo_says.packs import validate_pack

        data = _valid_pack_data(quotes="not-a-list")
        errors = validate_pack(data)
        assert len(errors) > 0
        assert any("quotes" in e.lower() for e in errors)

    def test_validate_pack_invalid_quotes_missing_text_category(self):
        """Quotes entries missing 'text' or 'category' should be flagged."""
        from neo_says.packs import validate_pack

        data = _valid_pack_data(quotes=[{"tags": ["x"]}])
        errors = validate_pack(data)
        assert len(errors) > 0
        combined = " ".join(errors).lower()
        assert "text" in combined or "category" in combined


# ---------------------------------------------------------------------------
# load_pack
# ---------------------------------------------------------------------------

class TestLoadPack:

    def test_load_pack_success(self, tmp_path):
        """Loading a valid YAML pack file returns the parsed dict."""
        from neo_says.packs import load_pack

        pack_data = _valid_pack_data()
        pack_file = _write_pack_yaml(tmp_path / "good.yaml", pack_data)

        result = load_pack(pack_file)
        assert isinstance(result, dict)
        assert result["name"] == "test-pack"
        assert isinstance(result["quotes"], list)
        assert len(result["quotes"]) == 1
        assert result["quotes"][0]["text"] == "Test quote"

    def test_load_pack_invalid(self, tmp_path):
        """Loading a pack that fails validation should raise ValueError."""
        from neo_says.packs import load_pack

        bad_data = {"name": "bad"}  # missing quotes, etc.
        bad_file = _write_pack_yaml(tmp_path / "bad.yaml", bad_data)

        with pytest.raises(ValueError):
            load_pack(bad_file)


# ---------------------------------------------------------------------------
# install_pack
# ---------------------------------------------------------------------------

class TestInstallPack:

    def test_install_pack(self, packs_dir, tmp_path):
        """install_pack copies a valid YAML file into the packs directory."""
        from neo_says.packs import install_pack

        source = _write_pack_yaml(tmp_path / "cool-pack.yaml", _valid_pack_data(name="cool-pack"))

        pack_name = install_pack(source)
        assert pack_name == "cool-pack"

        installed = list(packs_dir.glob("*.yaml")) + list(packs_dir.glob("*.yml"))
        assert len(installed) == 1
        # Verify the content survived the copy
        loaded = yaml.safe_load(installed[0].read_text(encoding="utf-8"))
        assert loaded["name"] == "cool-pack"

    def test_install_pack_not_found(self, packs_dir):
        """Installing from a non-existent file raises FileNotFoundError."""
        from neo_says.packs import install_pack

        with pytest.raises(FileNotFoundError):
            install_pack(Path("/tmp/definitely-does-not-exist-12345.yaml"))

    def test_install_pack_wrong_extension(self, packs_dir, tmp_path):
        """Installing a file without .yaml/.yml extension raises ValueError."""
        from neo_says.packs import install_pack

        txt_file = tmp_path / "pack.txt"
        txt_file.write_text("name: x", encoding="utf-8")

        with pytest.raises(ValueError):
            install_pack(txt_file)


# ---------------------------------------------------------------------------
# list_packs
# ---------------------------------------------------------------------------

class TestListPacks:

    def test_list_packs_empty(self, packs_dir):
        """An empty packs directory yields an empty list."""
        from neo_says.packs import list_packs

        result = list_packs()
        assert result == []

    def test_list_packs_with_packs(self, packs_dir):
        """Installed packs should appear with their metadata."""
        from neo_says.packs import list_packs

        pack_a = _valid_pack_data(name="alpha", author="Alice", version="1.0", description="Pack A")
        pack_b = _valid_pack_data(name="beta", author="Bob", version="2.0", description="Pack B")
        _write_pack_yaml(packs_dir / "alpha.yaml", pack_a)
        _write_pack_yaml(packs_dir / "beta.yaml", pack_b)

        result = list_packs()
        assert isinstance(result, list)
        assert len(result) == 2

        names = {p["name"] for p in result}
        assert names == {"alpha", "beta"}

        # Verify metadata keys are present
        for p in result:
            assert "name" in p
            assert "version" in p or "author" in p  # at least some metadata


# ---------------------------------------------------------------------------
# remove_pack
# ---------------------------------------------------------------------------

class TestRemovePack:

    def test_remove_pack_exists(self, packs_dir):
        """Removing an installed pack should delete its file and return True."""
        from neo_says.packs import remove_pack

        _write_pack_yaml(packs_dir / "doomed.yaml", _valid_pack_data(name="doomed"))
        assert (packs_dir / "doomed.yaml").exists()

        result = remove_pack("doomed")
        assert result is True
        assert not (packs_dir / "doomed.yaml").exists()

    def test_remove_pack_not_found(self, packs_dir):
        """Removing a non-existent pack should return False."""
        from neo_says.packs import remove_pack

        result = remove_pack("ghost-pack")
        assert result is False


# ---------------------------------------------------------------------------
# get_pack_quotes
# ---------------------------------------------------------------------------

class TestGetPackQuotes:

    def test_get_pack_quotes_all(self, packs_dir):
        """With no name filter, quotes from all installed packs are returned."""
        from neo_says.packs import get_pack_quotes

        pack_a = _valid_pack_data(
            name="alpha",
            quotes=[
                {"text": "Quote A1", "category": "cat-a", "tags": [], "weight": 1},
                {"text": "Quote A2", "category": "cat-a", "tags": [], "weight": 1},
            ],
        )
        pack_b = _valid_pack_data(
            name="beta",
            quotes=[
                {"text": "Quote B1", "category": "cat-b", "tags": [], "weight": 2},
            ],
        )
        _write_pack_yaml(packs_dir / "alpha.yaml", pack_a)
        _write_pack_yaml(packs_dir / "beta.yaml", pack_b)

        quotes = get_pack_quotes()
        assert isinstance(quotes, list)
        assert len(quotes) == 3
        texts = {q["text"] for q in quotes}
        assert texts == {"Quote A1", "Quote A2", "Quote B1"}

    def test_get_pack_quotes_specific(self, packs_dir):
        """Requesting a specific pack name returns only that pack's quotes."""
        from neo_says.packs import get_pack_quotes

        pack_a = _valid_pack_data(
            name="alpha",
            quotes=[{"text": "Alpha only", "category": "a", "tags": [], "weight": 1}],
        )
        pack_b = _valid_pack_data(
            name="beta",
            quotes=[{"text": "Beta only", "category": "b", "tags": [], "weight": 1}],
        )
        _write_pack_yaml(packs_dir / "alpha.yaml", pack_a)
        _write_pack_yaml(packs_dir / "beta.yaml", pack_b)

        quotes = get_pack_quotes(name="alpha")
        assert isinstance(quotes, list)
        assert len(quotes) == 1
        assert quotes[0]["text"] == "Alpha only"

    def test_get_pack_quotes_not_found(self, packs_dir):
        """Requesting quotes from a non-existent pack raises FileNotFoundError."""
        from neo_says.packs import get_pack_quotes

        with pytest.raises(FileNotFoundError):
            get_pack_quotes(name="no-such-pack")


# ---------------------------------------------------------------------------
# ensure_packs_dir
# ---------------------------------------------------------------------------

class TestEnsurePacksDir:

    def test_ensure_packs_dir_creates(self, tmp_path, monkeypatch):
        """ensure_packs_dir creates the directory if it does not exist."""
        from neo_says.packs import ensure_packs_dir

        target = tmp_path / "new_packs"
        assert not target.exists()
        monkeypatch.setattr("neo_says.packs.PACKS_DIR", target)

        ensure_packs_dir()
        assert target.is_dir()

    def test_ensure_packs_dir_idempotent(self, tmp_path, monkeypatch):
        """Calling ensure_packs_dir when it already exists should not fail."""
        from neo_says.packs import ensure_packs_dir

        target = tmp_path / "existing_packs"
        target.mkdir()
        monkeypatch.setattr("neo_says.packs.PACKS_DIR", target)

        ensure_packs_dir()  # should not raise
        assert target.is_dir()
