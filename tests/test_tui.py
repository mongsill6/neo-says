import pytest


def test_tui_module_imports():
    from neo_says.tui import NeoSaysTUI, run_tui
    assert NeoSaysTUI is not None
    assert run_tui is not None


def test_tui_app_creation():
    from neo_says.tui import NeoSaysTUI
    app = NeoSaysTUI()
    assert app is not None


def test_run_tui_is_callable():
    from neo_says.tui import run_tui
    assert callable(run_tui)
