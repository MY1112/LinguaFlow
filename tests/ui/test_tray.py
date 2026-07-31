"""系统托盘菜单行为测试。"""

from __future__ import annotations

from PySide6.QtWidgets import QApplication

from ui.tray import LFTrayMenu, Tray


def _qt_application() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_tray_menu_contains_current_actions() -> None:
    _qt_application()

    menu = LFTrayMenu()

    assert [action.objectName() for action in menu.actions() if action.objectName()] == [
        "title_action",
        "open_action",
        "pause_action",
        "settings_action",
        "exit_action",
    ]


def test_tray_exposes_pause_state() -> None:
    _qt_application()

    tray = Tray()

    assert tray.menu.pause_action.isEnabled()
    assert tray.menu.pause_action.text() == "暂停划词翻译"

    tray.set_paused(True)

    assert tray.menu.pause_action.text() == "恢复划词翻译"


def test_tray_menu_emits_open_request() -> None:
    _qt_application()
    tray = Tray()
    requested: list[bool] = []
    tray.show_requested.connect(lambda: requested.append(True))

    tray.menu.open_action.trigger()

    assert requested == [True]
