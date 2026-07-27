"""应用配置访问服务。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.logger import get_logger


class ConfigService:
    """负责加载、读取和保存应用配置。"""

    def __init__(self, config_directory: Path) -> None:
        self.config_directory = Path(config_directory)
        self._logger = get_logger(__name__)
        self._settings = self._load_json("settings.json", {"app": {"name": "LinguaFlow"}})
        self._hotkeys = self._load_json("hotkey.json", {})

    @property
    def settings(self) -> dict[str, Any]:
        return self._settings

    @property
    def hotkeys(self) -> dict[str, Any]:
        return self._hotkeys

    def get(self, key: str, default: Any = None) -> Any:
        """使用点号键读取配置，例如 ``app.name``。"""
        value: Any = self._settings
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, value: Any) -> None:
        """使用点号键设置配置，例如 ``app.name``。"""
        parts = key.split(".")
        target = self._settings
        for part in parts[:-1]:
            child = target.get(part)
            if not isinstance(child, dict):
                child = {}
                target[part] = child
            target = child
        target[parts[-1]] = value

    def save(self) -> None:
        """将设置和快捷键配置持久化到配置目录。"""
        self.config_directory.mkdir(parents=True, exist_ok=True)
        self._save_json("settings.json", self._settings)
        self._save_json("hotkey.json", self._hotkeys)

    def _load_json(self, filename: str, default: dict[str, Any]) -> dict[str, Any]:
        path = self.config_directory / filename
        if not path.exists():
            return default.copy()
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            self._logger.warning("无法加载配置 %s：%s", path, error)
            return default.copy()
        return data if isinstance(data, dict) else default.copy()

    def _save_json(self, filename: str, data: dict[str, Any]) -> None:
        path = self.config_directory / filename
        try:
            with path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
        except OSError as error:
            self._logger.error("无法保存配置 %s：%s", path, error)
            raise
