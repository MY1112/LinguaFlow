"""Settings 页面配置集成测试。"""

from __future__ import annotations

import json

import pytest
from PySide6.QtWidgets import QApplication

from services.config_service import ConfigService
from ui.settings.settings_window import SettingsWindow


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    return QApplication.instance() or QApplication([])


@pytest.fixture
def config_service(tmp_path) -> ConfigService:
    (tmp_path / "settings.json").write_text(
        json.dumps(
            {
                "app": {
                    "name": "LinguaFlow Test",
                    "version": "v1.2.3",
                    "model_path": "models/test.gguf",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (tmp_path / "hotkey.json").write_text(
        json.dumps({"translate_selection": "Ctrl+Alt+T"}),
        encoding="utf-8",
    )
    return ConfigService(tmp_path)


def test_settings_pages_read_values_from_config_service(
    qt_application: QApplication,
    config_service: ConfigService,
) -> None:
    window = SettingsWindow(config_service=config_service)

    assert window.pages["general"].app_name_label.text() == "LinguaFlow Test"
    assert window.pages["shortcut"].shortcut_label.text() == "Ctrl+Alt+T"
    assert window.pages["model"].model_path_label.text() == "models/test.gguf"
    assert window.pages["model"].model_status_label.text() == "Configured"
    assert window.pages["about"].version_label.text() == "v1.2.3"

    window.close()
