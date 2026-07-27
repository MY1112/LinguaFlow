"""HotkeyAdapter VoidPtr 消息测试。"""

from __future__ import annotations

import ctypes
import logging
from ctypes import wintypes

from integrations.hotkey import HotkeyAdapter


def test_native_event_filter_accepts_void_pointer_message() -> None:
    """PySide6 的 VoidPtr 原生消息应能触发快捷键回调。"""
    triggered: list[bool] = []
    adapter = HotkeyAdapter(lambda: triggered.append(True), logging.getLogger("test.hotkey"))
    message = wintypes.MSG()
    message.message = adapter._WM_HOTKEY
    message.wParam = adapter._HOTKEY_ID

    handled, result = adapter.nativeEventFilter(
        b"windows_generic_MSG",
        ctypes.c_void_p(ctypes.addressof(message)),
    )

    assert handled is True
    assert result == 0
    assert triggered == [True]
