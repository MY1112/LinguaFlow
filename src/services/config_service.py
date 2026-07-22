"""Application configuration access."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigService:
    """Loads application settings and hotkey configuration from one directory."""

    def __init__(self, config_directory: Path) -> None:
        self.config_directory = Path(config_directory)
        self._settings = self._load_json("settings.json", {"app": {"name": "LinguaFlow"}})
        self._hotkeys = self._load_json("hotkey.json", {})

    @property
    def settings(self) -> dict[str, Any]:
        return self._settings

    @property
    def hotkeys(self) -> dict[str, Any]:
        return self._hotkeys

    def get(self, key: str, default: Any = None) -> Any:
        """Read a setting using a dotted key such as ``app.name``."""
        value: Any = self._settings
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def _load_json(self, filename: str, default: dict[str, Any]) -> dict[str, Any]:
        path = self.config_directory / filename
        if not path.exists():
            return default.copy()
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return default.copy()
        return data if isinstance(data, dict) else default.copy()
