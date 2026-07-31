"""SettingsWindow 与 Application 的基础集成测试。"""

from __future__ import annotations

from unittest.mock import Mock

from app.application import Application


def test_application_shows_settings_window() -> None:
    application = Application.__new__(Application)
    application.settings_window = Mock()

    application._show_settings_window()

    application.settings_window.show.assert_called_once_with()
    application.settings_window.raise_.assert_called_once_with()
    application.settings_window.activateWindow.assert_called_once_with()
