"""系统托盘菜单行为测试。"""

from __future__ import annotations

from PySide6.QtWidgets import QApplication

from ui.tray import LFTrayMenu, Tray


def _qt_application() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_tray_menu_contains_required_actions() -> None:
    _qt_application()

    menu = LFTrayMenu()

    assert [action.objectName() for action in menu.actions()] == [
        "open_action",
        "translate_selection_action",
        "pause_action",
        "settings_action",
        "about_action",
        "exit_action",
    ]


def test_tray_exposes_menu_actions_and_pause_state() -> None:
    _qt_application()

    tray = Tray()

    assert tray.menu.translate_selection_action.isEnabled()
    assert tray.menu.pause_action.text() == "Pause"

    tray.set_paused(True)

    assert tray.menu.pause_action.text() == "Resume"


def test_tray_menu_emits_translate_selection_request() -> None:
    _qt_application()
    tray = Tray()
    requested: list[bool] = []
    tray.translate_selection_requested.connect(lambda: requested.append(True))

    tray.menu.translate_selection_action.trigger()

    assert requested == [True]
