"""Tests for CLI interface."""

import subprocess
import sys


class TestCLI:
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "neo_says", *args],
            capture_output=True, text=True,
            cwd="/tmp/neo-says",
            env={"PYTHONPATH": "/tmp/neo-says/src", "PATH": ""},
        )

    def test_help_flag(self):
        result = self._run("--help")
        assert result.returncode == 0
        assert "Snarky developer wisdom" in result.stdout

    def test_list_categories(self):
        result = self._run("--list-categories")
        assert result.returncode == 0
        assert "git" in result.stdout
        assert "debugging" in result.stdout

    def test_list_tags(self):
        result = self._run("--list-tags")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_raw_output(self):
        result = self._run("--raw")
        assert result.returncode == 0
        assert "╭" not in result.stdout

    def test_category_filter(self):
        result = self._run("-c", "git", "--raw")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_tag_filter(self):
        result = self._run("-t", "humor", "--raw")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_today_quote(self):
        result = self._run("--today", "--raw")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_today_is_deterministic(self):
        r1 = self._run("--today", "--raw")
        r2 = self._run("--today", "--raw")
        assert r1.stdout == r2.stdout

    def test_default_output_has_box(self):
        result = self._run()
        assert result.returncode == 0
        assert "╭" in result.stdout
