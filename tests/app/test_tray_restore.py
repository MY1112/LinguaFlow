"""托盘打开主窗口的回归测试。"""

from __future__ import annotations

from unittest.mock import Mock

from app.application import Application


def test_show_window_restores_minimized_main_window() -> None:
    application = Application.__new__(Application)
    application.main_window = Mock()

    application._show_window()

    application.main_window.showNormal.assert_called_once_with()
    application.main_window.show.assert_called_once_with()
    application.main_window.raise_.assert_called_once_with()
    application.main_window.activateWindow.assert_called_once_with()
