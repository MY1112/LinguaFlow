"""SelectionAdapter Windows INPUT 布局测试。"""

from __future__ import annotations

import ctypes

from integrations.selection import _INPUT


def test_windows_input_structure_has_expected_size() -> None:
    """64 位 Windows 的 INPUT 结构体应为 40 字节。"""
    assert ctypes.sizeof(_INPUT) == 40
