"""Tests for CLI interface."""

import subprocess
import sys


class TestCLI:
    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, "-m", "neo_says", "--help"],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env={"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""},
        )
        assert result.returncode == 0
        assert "Snarky developer wisdom" in result.stdout

    def test_list_categories(self):
        result = subprocess.run(
            [sys.executable, "-m", "neo_says", "--list-categories"],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env={"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""},
        )
        assert result.returncode == 0
        assert "git" in result.stdout
        assert "debugging" in result.stdout

    def test_raw_output(self):
        result = subprocess.run(
            [sys.executable, "-m", "neo_says", "--raw"],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env={"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""},
        )
        assert result.returncode == 0
        assert "╭" not in result.stdout  # no box in raw mode

    def test_category_filter(self):
        result = subprocess.run(
            [sys.executable, "-m", "neo_says", "-c", "git", "--raw"],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env={"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""},
        )
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_default_output_has_box(self):
        result = subprocess.run(
            [sys.executable, "-m", "neo_says"],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env={"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""},
        )
        assert result.returncode == 0
        assert "╭" in result.stdout
