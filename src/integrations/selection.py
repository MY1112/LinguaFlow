"""Windows 选中文本适配器。"""

from __future__ import annotations

import ctypes
import logging
import sys
import threading
import time
from ctypes import wintypes

from PySide6.QtCore import QObject, Signal

from core.logger import get_logger


class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class _HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", _MOUSEINPUT),
        ("ki", _KEYBDINPUT),
        ("hi", _HARDWAREINPUT),
    ]


class _INPUT(ctypes.Structure):
    _anonymous_ = ("union",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", _INPUT_UNION),
    ]


class SelectionAdapter(QObject):
    """通过 Windows 原生输入与剪贴板 API 获取选中文本。"""

    capture_finished = Signal(str)

    _INPUT_KEYBOARD = 1
    _CF_UNICODETEXT = 13
    _GMEM_MOVEABLE = 0x0002
    _VK_CONTROL = 0x11
    _VK_MENU = 0x12
    _VK_SHIFT = 0x10
    _VK_LCONTROL = 0xA2
    _VK_LMENU = 0xA4
    _VK_LSHIFT = 0xA0
    _VK_LWIN = 0x5B
    _VK_RWIN = 0x5C
    _VK_C = 0x43
    _VK_Q = 0x51
    _KEYEVENTF_KEYUP = 0x0002
    _KEYEVENTF_SCANCODE = 0x0008
    _MAPVK_VK_TO_VSC = 0
    _HOTKEY_KEYS = (_VK_MENU, _VK_Q)
    _MODIFIER_KEYS = (_VK_CONTROL, _VK_MENU, _VK_SHIFT, _VK_LWIN, _VK_RWIN)
    _COPY_MAX_ATTEMPTS = 4
    _HOTKEY_RELEASE_TIMEOUT = 1.5
    _COPY_TIMEOUT = 1.8
    _COPY_RETRY_INTERVAL = 0.15
    _CLIPBOARD_POLL_INTERVAL = 0.05
    _FOREGROUND_SETTLE_DELAY = 0.02
    _SENTINEL_PREFIX = "__linguaflow_clipboard_sentinel__"

    def __init__(self, logger: logging.Logger | None = None) -> None:
        super().__init__()
        self._logger = logger or get_logger(__name__)
        self._capture_thread: threading.Thread | None = None

    def get_selected_text(self, foreground_hwnd: int | None = None) -> str:
        """同步获取选中文本，供捕获线程调用。"""
        return self._capture_selected_text(foreground_hwnd)

    def capture_selected_text(self, foreground_hwnd: int | None = None) -> bool:
        """异步获取选中文本并通过 Signal 返回结果。"""
        if self._capture_thread is not None and self._capture_thread.is_alive():
            self._logger.warning("选中文本捕获任务正在执行")
            return False

        def capture() -> None:
            try:
                self.capture_finished.emit(self.get_selected_text(foreground_hwnd))
            finally:
                self._capture_thread = None

        self._capture_thread = threading.Thread(
            target=capture,
            name="linguaflow-selection-capture",
            daemon=True,
        )
        self._capture_thread.start()
        return True

    def _capture_selected_text(self, foreground_hwnd: int | None = None) -> str:
        """获取当前前台窗口中的选中文本，失败时返回空字符串。"""
        if sys.platform != "win32":
            self._logger.warning("获取选中文本仅支持 Windows")
            return ""

        previous_text: str | None = None
        foreground_hwnd = foreground_hwnd or 0
        try:
            previous_text = self._read_clipboard_text()
            foreground_hwnd = foreground_hwnd or self._get_foreground_window()
            sentinel = f"{self._SENTINEL_PREFIX}{time.time_ns()}__"
            self._write_clipboard_text(sentinel)
            sequence_before = self._get_clipboard_sequence()
            time.sleep(self._COPY_RETRY_INTERVAL)

            deadline = time.monotonic() + self._COPY_TIMEOUT
            attempts = 0
            last_send = 0.0
            while time.monotonic() < deadline:
                now = time.monotonic()
                if (
                    attempts < self._COPY_MAX_ATTEMPTS
                    and now - last_send >= self._COPY_RETRY_INTERVAL
                ):
                    self._send_copy_hotkey(foreground_hwnd)
                    attempts += 1
                    last_send = time.monotonic()

                if self._get_clipboard_sequence() != sequence_before:
                    selected_text = self._read_clipboard_text()
                    if selected_text != sentinel:
                        self._logger.info("获取选中文本，长度：%d", len(selected_text))
                        return selected_text
                time.sleep(self._CLIPBOARD_POLL_INTERVAL)

            return ""
        except Exception as error:
            self._logger.error("获取选中文本失败：%s", error)
            return ""
        finally:
            if previous_text is not None:
                try:
                    self._write_clipboard_text(previous_text)
                except Exception as error:
                    self._logger.warning("恢复剪贴板文本失败：%s", error)

    def _get_clipboard_sequence(self) -> int:
        user32 = ctypes.windll.user32
        user32.GetClipboardSequenceNumber.restype = ctypes.c_uint
        return user32.GetClipboardSequenceNumber()

    def _get_foreground_window(self) -> int:
        user32 = ctypes.windll.user32
        user32.GetForegroundWindow.argtypes = []
        user32.GetForegroundWindow.restype = wintypes.HWND
        return int(user32.GetForegroundWindow() or 0)

    def _attach_foreground_thread(self, foreground_hwnd: int) -> tuple[int, int] | None:
        if not foreground_hwnd:
            return None

        user32 = ctypes.windll.user32
        user32.GetWindowThreadProcessId.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(wintypes.DWORD),
        ]
        user32.GetWindowThreadProcessId.restype = wintypes.DWORD
        kernel32 = ctypes.windll.kernel32
        kernel32.GetCurrentThreadId.argtypes = []
        kernel32.GetCurrentThreadId.restype = wintypes.DWORD
        user32.AttachThreadInput.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.BOOL]
        user32.AttachThreadInput.restype = wintypes.BOOL

        process_id = wintypes.DWORD(0)
        foreground_thread = int(
            user32.GetWindowThreadProcessId(foreground_hwnd, ctypes.byref(process_id))
        )
        current_thread = int(kernel32.GetCurrentThreadId())
        if not foreground_thread or foreground_thread == current_thread:
            return None
        if not user32.AttachThreadInput(foreground_thread, current_thread, True):
            self._logger.warning("附加前台窗口输入线程失败：%d", ctypes.get_last_error())
            return None
        return foreground_thread, current_thread

    def _detach_foreground_thread(self, foreground_thread: int, current_thread: int) -> None:
        user32 = ctypes.windll.user32
        user32.AttachThreadInput.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.BOOL]
        user32.AttachThreadInput.restype = wintypes.BOOL
        user32.AttachThreadInput(foreground_thread, current_thread, False)

    def _set_foreground_window(self, foreground_hwnd: int) -> None:
        user32 = ctypes.windll.user32
        user32.SetForegroundWindow.argtypes = [wintypes.HWND]
        user32.SetForegroundWindow.restype = wintypes.BOOL
        user32.SetForegroundWindow(foreground_hwnd)

    def _wait_for_modifiers_release(self) -> None:
        user32 = ctypes.windll.user32
        user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
        user32.GetAsyncKeyState.restype = ctypes.c_short
        deadline = time.monotonic() + self._HOTKEY_RELEASE_TIMEOUT
        while time.monotonic() < deadline:
            if not any(user32.GetAsyncKeyState(key) & 0x8000 for key in self._MODIFIER_KEYS):
                return
            time.sleep(self._CLIPBOARD_POLL_INTERVAL)
        self._logger.warning("修饰键未在限定时间内释放，继续复制")

    def _release_stale_modifiers(self) -> None:
        try:
            self._send_keyboard_inputs(self._build_modifier_release_inputs())
        except OSError as error:
            self._logger.warning("释放残留修饰键失败：%s", error)
        time.sleep(self._FOREGROUND_SETTLE_DELAY)

    @classmethod
    def _build_copy_inputs(cls) -> _INPUT * 4:
        """构造使用扫描码的 Ctrl+C 输入序列。"""
        inputs = (_INPUT * 4)()
        events = (
            (cls._VK_LCONTROL, 0),
            (cls._VK_C, 0),
            (cls._VK_C, cls._KEYEVENTF_KEYUP),
            (cls._VK_LCONTROL, cls._KEYEVENTF_KEYUP),
        )
        for index, (virtual_key, flags) in enumerate(events):
            inputs[index] = cls._build_scan_input(virtual_key, flags)
        return inputs

    @classmethod
    def _build_modifier_release_inputs(cls) -> _INPUT * 3:
        inputs = (_INPUT * 3)()
        events = (
            (cls._VK_LMENU, cls._KEYEVENTF_KEYUP),
            (cls._VK_LCONTROL, cls._KEYEVENTF_KEYUP),
            (cls._VK_LSHIFT, cls._KEYEVENTF_KEYUP),
        )
        for index, (virtual_key, flags) in enumerate(events):
            inputs[index] = cls._build_scan_input(virtual_key, flags)
        return inputs

    @classmethod
    def _build_scan_input(cls, virtual_key: int, flags: int) -> _INPUT:
        user32 = ctypes.windll.user32
        user32.MapVirtualKeyW.argtypes = [wintypes.UINT, wintypes.UINT]
        user32.MapVirtualKeyW.restype = wintypes.UINT
        scan_code = user32.MapVirtualKeyW(virtual_key, cls._MAPVK_VK_TO_VSC)
        return _INPUT(
            cls._INPUT_KEYBOARD,
            _INPUT_UNION(
                ki=_KEYBDINPUT(
                    0,
                    scan_code,
                    cls._KEYEVENTF_SCANCODE | flags,
                    0,
                    0,
                )
            ),
        )

    def _send_copy_hotkey(self, foreground_hwnd: int) -> None:
        """向目标前台窗口发送一次干净的 Ctrl+C。"""
        attached_threads = self._attach_foreground_thread(foreground_hwnd)
        try:
            if foreground_hwnd:
                self._set_foreground_window(foreground_hwnd)
                time.sleep(self._FOREGROUND_SETTLE_DELAY)
            self._wait_for_modifiers_release()
            self._release_stale_modifiers()
            self._send_keyboard_inputs(self._build_copy_inputs())
            time.sleep(0.03)
        finally:
            if attached_threads is not None:
                self._detach_foreground_thread(*attached_threads)

    def _send_keyboard_inputs(self, inputs: ctypes.Array) -> None:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.SendInput.argtypes = [
            wintypes.UINT,
            ctypes.POINTER(_INPUT),
            ctypes.c_int,
        ]
        user32.SendInput.restype = wintypes.UINT
        sent_count = user32.SendInput(len(inputs), inputs, ctypes.sizeof(_INPUT))
        if sent_count != len(inputs):
            last_error = ctypes.get_last_error()
            raise OSError(f"SendInput failed: {sent_count}, last_error: {last_error}")

    def _configure_clipboard_api(self, user32: object, kernel32: object) -> None:
        user32.OpenClipboard.argtypes = [ctypes.c_void_p]
        user32.OpenClipboard.restype = ctypes.c_int
        user32.CloseClipboard.argtypes = []
        user32.CloseClipboard.restype = ctypes.c_int
        user32.GetClipboardData.argtypes = [ctypes.c_uint]
        user32.GetClipboardData.restype = ctypes.c_void_p
        user32.EmptyClipboard.argtypes = []
        user32.EmptyClipboard.restype = ctypes.c_int
        user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
        user32.SetClipboardData.restype = ctypes.c_void_p
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalUnlock.restype = ctypes.c_int
        kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
        kernel32.GlobalAlloc.restype = ctypes.c_void_p
        kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
        kernel32.GlobalFree.restype = ctypes.c_void_p

    def _read_clipboard_text(self) -> str:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        self._configure_clipboard_api(user32, kernel32)
        if not user32.OpenClipboard(None):
            raise OSError("OpenClipboard failed")
        try:
            handle = user32.GetClipboardData(self._CF_UNICODETEXT)
            if not handle:
                return ""
            pointer = kernel32.GlobalLock(handle)
            if not pointer:
                raise OSError("GlobalLock failed")
            try:
                return ctypes.wstring_at(pointer)
            finally:
                kernel32.GlobalUnlock(handle)
        finally:
            user32.CloseClipboard()

    def _write_clipboard_text(self, text: str) -> None:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        self._configure_clipboard_api(user32, kernel32)
        if not user32.OpenClipboard(None):
            raise OSError("OpenClipboard failed")
        handle = None
        try:
            encoded_text = (text + "\x00").encode("utf-16-le")
            handle = kernel32.GlobalAlloc(self._GMEM_MOVEABLE, len(encoded_text))
            if not handle:
                raise OSError("GlobalAlloc failed")
            pointer = kernel32.GlobalLock(handle)
            if not pointer:
                raise OSError("GlobalLock failed")
            try:
                ctypes.memmove(pointer, encoded_text, len(encoded_text))
            finally:
                kernel32.GlobalUnlock(handle)
            if not user32.EmptyClipboard():
                raise OSError("EmptyClipboard failed")
            if not user32.SetClipboardData(self._CF_UNICODETEXT, handle):
                raise OSError("SetClipboardData failed")
            handle = None
        finally:
            if handle:
                kernel32.GlobalFree(handle)
            user32.CloseClipboard()
