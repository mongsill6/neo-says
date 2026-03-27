"""Quote pack management for neo-says.

Supports YAML-based custom quote packs stored in ~/.neo-says/packs/.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml  # We'll need PyYAML

PACKS_DIR: Path = Path.home() / ".neo-says" / "packs"

REQUIRED_FIELDS = {"name", "version", "quotes"}


def ensure_packs_dir() -> Path:
    """Create the packs directory if it doesn't exist."""
    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    return PACKS_DIR


def validate_pack(data: Dict[str, Any]) -> List[str]:
    """Validate a pack's structure. Return list of error messages (empty = valid)."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "quotes" in data:
        if not isinstance(data["quotes"], list):
            errors.append("'quotes' must be a list")
        else:
            for i, q in enumerate(data["quotes"]):
                if not isinstance(q, dict):
                    errors.append(f"Quote #{i} must be a mapping")
                    continue
                if "text" not in q:
                    errors.append(f"Quote #{i} missing 'text' field")
                if "category" not in q:
                    errors.append(f"Quote #{i} missing 'category' field")

    return errors


def load_pack(path: Path) -> Dict[str, Any]:
    """Load and validate a single YAML pack file.

    Raises ValueError if the pack is invalid.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Pack file must contain a YAML mapping: {path}")

    errors = validate_pack(data)
    if errors:
        raise ValueError(f"Invalid pack '{path.name}': {'; '.join(errors)}")

    return data


def list_packs() -> List[Dict[str, Any]]:
    """List all installed packs with their metadata."""
    ensure_packs_dir()
    packs = []
    for pack_file in sorted(PACKS_DIR.glob("*.yaml")):
        try:
            data = load_pack(pack_file)
            packs.append({
                "name": data["name"],
                "version": data.get("version", "unknown"),
                "author": data.get("author", "unknown"),
                "description": data.get("description", ""),
                "quotes_count": len(data.get("quotes", [])),
                "path": str(pack_file),
            })
        except (ValueError, yaml.YAMLError):
            continue
    return packs


def install_pack(source: str) -> str:
    """Install a pack from a file path.

    Returns the installed pack name.
    Raises FileNotFoundError or ValueError on failure.
    """
    source_path = Path(source).expanduser().resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"Pack file not found: {source}")

    if not source_path.suffix in (".yaml", ".yml"):
        raise ValueError("Pack file must be a .yaml or .yml file")

    data = load_pack(source_path)
    pack_name = data["name"]

    ensure_packs_dir()
    dest = PACKS_DIR / f"{pack_name}.yaml"
    shutil.copy2(source_path, dest)

    return pack_name


def remove_pack(name: str) -> bool:
    """Remove an installed pack by name.

    Returns True if removed, False if not found.
    """
    ensure_packs_dir()
    pack_file = PACKS_DIR / f"{name}.yaml"
    if pack_file.exists():
        pack_file.unlink()
        return True
    return False


def get_pack_quotes(name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get quotes from installed packs.

    If name is provided, get quotes from that specific pack only.
    If name is None, get quotes from ALL installed packs.
    """
    ensure_packs_dir()
    all_quotes = []

    if name:
        pack_file = PACKS_DIR / f"{name}.yaml"
        if not pack_file.exists():
            raise FileNotFoundError(f"Pack '{name}' not found")
        data = load_pack(pack_file)
        for q in data.get("quotes", []):
            q.setdefault("tags", [])
            q.setdefault("weight", 3)
            all_quotes.append(q)
    else:
        for pack_file in sorted(PACKS_DIR.glob("*.yaml")):
            try:
                data = load_pack(pack_file)
                for q in data.get("quotes", []):
                    q.setdefault("tags", [])
                    q.setdefault("weight", 3)
                    all_quotes.append(q)
            except (ValueError, yaml.YAMLError):
                continue

    return all_quotes
