"""HotkeyAdapter 的热键绑定测试。"""

from __future__ import annotations

from integrations.hotkey import HotkeyAdapter


def test_default_hotkey_is_alt_q() -> None:
    """默认快捷键应为 Alt + Q。"""
    assert HotkeyAdapter._MOD_ALT == 0x0001
    assert HotkeyAdapter._VK_Q == 0x51


def test_hotkey_can_bind_to_application_window() -> None:
    """全局热键应绑定到 Application 提供的窗口句柄。"""
    adapter = HotkeyAdapter(window_handle=1234)

    assert adapter._window_handle == 1234
