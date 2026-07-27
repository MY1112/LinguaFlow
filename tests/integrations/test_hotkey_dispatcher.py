"""HotkeyAdapter dispatcher 事件测试。"""

from __future__ import annotations

import ctypes
import logging
from ctypes import wintypes

from integrations.hotkey import HotkeyAdapter


def test_native_event_filter_accepts_windows_dispatcher_messages() -> None:
    """线程级 RegisterHotKey 消息应通过 dispatcher 事件触发回调。"""
    triggered: list[bool] = []
    adapter = HotkeyAdapter(lambda: triggered.append(True), logging.getLogger("test.hotkey"))
    message = wintypes.MSG()
    message.message = adapter._WM_HOTKEY
    message.wParam = adapter._HOTKEY_ID

    handled, result = adapter.nativeEventFilter(
        b"windows_dispatcher_MSG",
        ctypes.addressof(message),
    )

    assert handled is True
    assert result == 0
    assert triggered == [True]
