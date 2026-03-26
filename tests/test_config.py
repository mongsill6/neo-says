import pytest

from neo_says.config import get_config, get_default_author, get_default_theme, set_config


@pytest.fixture(autouse=True)
def _use_tmp_config(tmp_path, monkeypatch):
    config_path = tmp_path / ".neo-says.toml"
    monkeypatch.setattr("neo_says.config.CONFIG_PATH", config_path)


def test_get_config_defaults():
    config = get_config()
    assert config["display"]["theme"] == "box"
    assert config["display"]["author"] == "Neo"


def test_get_default_theme():
    assert get_default_theme() == "box"


def test_get_default_author():
    assert get_default_author() == "Neo"


def test_set_and_get_config():
    set_config("display.theme", "minimal")
    assert get_config()["display"]["theme"] == "minimal"


def test_config_persistence():
    set_config("display.theme", "cowsay")
    set_config("display.author", "Morpheus")
    config = get_config()
    assert config["display"]["theme"] == "cowsay"
    assert config["display"]["author"] == "Morpheus"
