"""Application 划词翻译调度测试。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from app.application import Application


def test_hotkey_schedules_selection_after_native_event(monkeypatch) -> None:
    """快捷键回调应将选中文本读取延后到 Qt 事件循环。"""
    application = Application.__new__(Application)
    application.context = SimpleNamespace(logger=Mock())
    application._translate_selection = Mock()

    from app import application as application_module

    monkeypatch.setattr(
        application_module.QTimer,
        "singleShot",
        lambda delay, callback: callback(),
    )

    application._schedule_selection_translation()

    application._translate_selection.assert_called_once_with()
