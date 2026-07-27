"""SelectionAdapter 的复制输入测试。"""

from __future__ import annotations

from integrations.selection import SelectionAdapter


def test_copy_input_sequence_uses_ctrl_c_scan_codes() -> None:
    """复制输入应使用扫描码按下并释放 Ctrl+C。"""
    inputs = SelectionAdapter._build_copy_inputs()

    assert len(inputs) == 4
    assert all(
        input_item.ki.dwFlags & SelectionAdapter._KEYEVENTF_SCANCODE for input_item in inputs
    )
    assert inputs[0].ki.wVk == 0
    assert inputs[1].ki.wVk == 0
    assert inputs[2].ki.wVk == 0
    assert inputs[3].ki.wVk == 0
    assert inputs[2].ki.dwFlags & SelectionAdapter._KEYEVENTF_KEYUP
    assert inputs[3].ki.dwFlags & SelectionAdapter._KEYEVENTF_KEYUP


def test_alt_modifier_key_code_is_defined() -> None:
    """等待快捷键释放需要使用 Windows Alt 虚拟键码。"""
    assert SelectionAdapter._VK_MENU == 0x12


def test_hotkey_release_waits_for_all_modifiers() -> None:
    """复制前应等待所有修饰键释放。"""
    assert SelectionAdapter._MODIFIER_KEYS == (
        SelectionAdapter._VK_CONTROL,
        SelectionAdapter._VK_MENU,
        SelectionAdapter._VK_SHIFT,
        SelectionAdapter._VK_LWIN,
        SelectionAdapter._VK_RWIN,
    )


def test_selection_copy_retries_are_bounded() -> None:
    """选中文本复制应限制重试次数，避免阻塞流程。"""
    assert SelectionAdapter._COPY_MAX_ATTEMPTS == 4


def test_selection_capture_emits_result_without_blocking_caller(monkeypatch) -> None:
    """异步捕获应在独立线程执行并通过 Signal 返回结果。"""
    import threading
    import time

    adapter = SelectionAdapter()
    caller_thread = threading.get_ident()
    capture_threads: list[int] = []
    results: list[str] = []
    finished = threading.Event()

    def capture(foreground_hwnd: int | None) -> str:
        capture_threads.append(threading.get_ident())
        time.sleep(0.05)
        return "Hello"

    monkeypatch.setattr(adapter, "_capture_selected_text", capture)
    from PySide6.QtCore import Qt

    adapter.capture_finished.connect(
        lambda text: (results.append(text), finished.set()),
        Qt.ConnectionType.DirectConnection,
    )

    started_at = time.monotonic()
    adapter.capture_selected_text(1234)
    elapsed = time.monotonic() - started_at

    assert elapsed < 0.04
    assert finished.wait(1)
    assert results == ["Hello"]
    assert capture_threads[0] != caller_thread
