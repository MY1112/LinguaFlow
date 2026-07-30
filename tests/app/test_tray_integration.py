"""托盘菜单与应用生命周期的连接测试。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from app.application import Application


def test_paused_application_does_not_schedule_selection_translation(monkeypatch) -> None:
    application = Application.__new__(Application)
    application._paused = True
    application.context = SimpleNamespace(logger=Mock())

    from app import application as application_module

    single_shot = Mock()
    monkeypatch.setattr(application_module.QTimer, "singleShot", single_shot)

    application._schedule_selection_translation()

    single_shot.assert_not_called()
    application.context.logger.info.assert_called_once()


def test_pause_toggle_unregisters_and_registers_hotkey() -> None:
    application = Application.__new__(Application)
    application._paused = False
    application.hotkey_adapter = Mock()
    application.tray = Mock()
    application.context = SimpleNamespace(logger=Mock())

    application._toggle_pause()
    application.hotkey_adapter.unregister.assert_called_once_with()
    application.tray.set_paused.assert_called_once_with(True)

    application._toggle_pause()
    application.hotkey_adapter.register.assert_called_once_with()
    application.tray.set_paused.assert_called_with(False)
