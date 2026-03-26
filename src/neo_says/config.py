"""User configuration management for neo-says.

Config file: ~/.neo-says.toml

Schema:
    [display]
    theme = "box"
    author = "Neo"
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

CONFIG_PATH: Path = Path.home() / ".neo-says.toml"

_DEFAULTS: Dict[str, Dict[str, str]] = {
    "display": {
        "theme": "box",
        "author": "Neo",
    },
}


def get_config() -> Dict[str, Any]:
    """Load configuration from ~/.neo-says.toml.

    Returns the merged config with defaults applied for any missing keys.
    If the config file does not exist, returns the default configuration.
    """
    config: Dict[str, Any] = {
        section: dict(values) for section, values in _DEFAULTS.items()
    }

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "rb") as f:
            file_config = tomllib.loads(f.read().decode("utf-8"))
        for section, values in file_config.items():
            if section in config and isinstance(values, dict):
                config[section].update(values)
            else:
                config[section] = values

    return config


def get_default_theme() -> str:
    """Return the configured default theme name."""
    config = get_config()
    return str(config["display"]["theme"])


def get_default_author() -> str:
    """Return the configured default author."""
    config = get_config()
    return str(config["display"]["author"])


def _write_config(config: Dict[str, Any]) -> None:
    """Write configuration dict to ~/.neo-says.toml using simple string formatting.

    Only supports a flat two-level structure (section -> key = value).
    """
    lines: list[str] = []
    for section, values in config.items():
        if not isinstance(values, dict):
            continue
        lines.append(f"[{section}]")
        for key, value in values.items():
            # Escape backslashes and double quotes in string values
            escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{key} = "{escaped}"')
        lines.append("")

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text("\n".join(lines), encoding="utf-8")


def set_config(key: str, value: str) -> None:
    """Set a config value and save to disk.

    Args:
        key: Dotted key path, e.g. ``"display.theme"`` or ``"display.author"``.
        value: The string value to set.

    Raises:
        ValueError: If *key* does not contain exactly one dot separator.
    """
    parts = key.split(".")
    if len(parts) != 2:
        raise ValueError(
            f"Key must be in 'section.name' format (e.g. 'display.theme'), got: {key!r}"
        )

    section, name = parts
    config = get_config()

    if section not in config:
        config[section] = {}
    config[section][name] = value

    _write_config(config)
