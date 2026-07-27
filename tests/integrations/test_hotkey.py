"""HotkeyAdapter 的 Windows 原生消息测试。"""

from __future__ import annotations

import ctypes
import logging
from ctypes import wintypes

from integrations.hotkey import HotkeyAdapter


def test_native_event_filter_accepts_pyside_qt6_message_capsule() -> None:
    """Qt6 的 PyCapsule 消息应能触发快捷键回调。"""
    triggered: list[bool] = []
    adapter = HotkeyAdapter(lambda: triggered.append(True), logging.getLogger("test.hotkey"))
    message = wintypes.MSG()
    message.message = adapter._WM_HOTKEY
    message.wParam = adapter._HOTKEY_ID

    capsule_new = ctypes.pythonapi.PyCapsule_New
    capsule_new.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
    capsule_new.restype = ctypes.py_object
    capsule = capsule_new(ctypes.addressof(message), None, None)

    handled, result = adapter.nativeEventFilter(b"windows_generic_MSG", capsule)

    assert handled is True
    assert result == 0
    assert triggered == [True]


def test_hotkey_keeps_last_external_window_when_own_window_is_foreground(monkeypatch) -> None:
    """LinguaFlow 自身窗口置前时不应覆盖上一次外部目标窗口。"""
    adapter = HotkeyAdapter(logger=logging.getLogger("test.hotkey"))
    adapter._last_foreground_window = 1234

    monkeypatch.setattr(adapter, "_get_foreground_window", lambda: 5678)
    monkeypatch.setattr(adapter, "_is_current_process_window", lambda hwnd: True)

    adapter._record_foreground_window()

    assert adapter.last_foreground_window == 1234
