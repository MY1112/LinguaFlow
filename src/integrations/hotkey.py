"""Windows 全局快捷键适配器。"""

from __future__ import annotations

import ctypes
import logging
import sys
from ctypes import wintypes
from typing import Callable

from PySide6.QtCore import QAbstractNativeEventFilter, QCoreApplication

from core.logger import get_logger


class HotkeyAdapter(QAbstractNativeEventFilter):
    """封装 Windows 全局快捷键的注册与注销。"""

    _HOTKEY_ID = 1
    _MOD_ALT = 0x0001
    _VK_Q = 0x51
    _WM_HOTKEY = 0x0312

    def __init__(
        self,
        on_triggered: Callable[[], None] | None = None,
        logger: logging.Logger | None = None,
        window_handle: int | None = None,
    ) -> None:
        super().__init__()
        self._logger = logger or get_logger(__name__)
        self._on_triggered = on_triggered
        self._window_handle = window_handle
        self._last_foreground_window = 0
        self._registered = False

    @property
    def last_foreground_window(self) -> int:
        """返回热键触发瞬间记录的前台窗口句柄。"""
        return self._last_foreground_window

    def register(self) -> bool:
        """注册 Alt + Q 全局快捷键。"""
        if self._registered:
            return True
        if sys.platform != "win32":
            self._logger.warning("全局快捷键仅支持 Windows")
            return False

        application = QCoreApplication.instance()
        if application is None:
            self._logger.error("无法注册快捷键：Qt 应用尚未初始化")
            return False

        user32 = ctypes.windll.user32
        target_window = wintypes.HWND(self._window_handle or 0)
        if not user32.RegisterHotKey(target_window, self._HOTKEY_ID, self._MOD_ALT, self._VK_Q):
            self._logger.error("注册全局快捷键失败：%s", ctypes.get_last_error())
            return False

        application.installNativeEventFilter(self)
        self._registered = True
        self._logger.info("已注册全局快捷键：Alt + Q")
        return True

    def unregister(self) -> None:
        """注销 Alt + Q 全局快捷键。"""
        if not self._registered:
            return
        application = QCoreApplication.instance()
        if application is not None:
            application.removeNativeEventFilter(self)
        if sys.platform == "win32":
            ctypes.windll.user32.UnregisterHotKey(
                wintypes.HWND(self._window_handle or 0), self._HOTKEY_ID
            )
        self._registered = False
        self._logger.info("已注销全局快捷键：Alt + Q")

    def nativeEventFilter(self, event_type: object, message: object) -> tuple[bool, int]:
        """捕获 Windows 原生快捷键消息并发送回调。"""
        if sys.platform != "win32" or event_type not in (
            b"windows_generic_MSG",
            b"windows_dispatcher_MSG",
        ):
            return False, 0
        try:
            message_pointer = self._get_message_pointer(message)
            native_message = ctypes.cast(
                message_pointer,
                ctypes.POINTER(wintypes.MSG),
            ).contents
        except (TypeError, ValueError, ctypes.ArgumentError):
            return False, 0
        if native_message.message != self._WM_HOTKEY:
            return False, 0
        if native_message.wParam != self._HOTKEY_ID:
            return False, 0

        self._record_foreground_window()
        self._logger.info("触发全局快捷键")
        if self._on_triggered is not None:
            self._on_triggered()
        return True, 0

    def _record_foreground_window(self) -> None:
        foreground_window = self._get_foreground_window()
        if not foreground_window:
            return
        if self._is_current_process_window(foreground_window):
            self._logger.warning("热键触发时前台窗口属于 LinguaFlow，沿用上次外部窗口")
            return
        self._last_foreground_window = foreground_window

    @staticmethod
    def _is_current_process_window(window_handle: int) -> bool:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        process_id = wintypes.DWORD(0)
        user32.GetWindowThreadProcessId.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(wintypes.DWORD),
        ]
        user32.GetWindowThreadProcessId.restype = wintypes.DWORD
        kernel32.GetCurrentProcessId.argtypes = []
        kernel32.GetCurrentProcessId.restype = wintypes.DWORD
        user32.GetWindowThreadProcessId(window_handle, ctypes.byref(process_id))
        return process_id.value == int(kernel32.GetCurrentProcessId())

    @staticmethod
    def _get_foreground_window() -> int:
        user32 = ctypes.windll.user32
        user32.GetForegroundWindow.argtypes = []
        user32.GetForegroundWindow.restype = wintypes.HWND
        return int(user32.GetForegroundWindow() or 0)

    @staticmethod
    def _get_message_pointer(message: object) -> int:
        """兼容 PySide6 Qt6 的原生消息指针。"""
        if isinstance(message, int):
            return message

        pointer_value = getattr(message, "value", None)
        if isinstance(pointer_value, int):
            if not pointer_value:
                raise ValueError("原生消息指针为空")
            return pointer_value

        try:
            pointer = int(message)
        except (TypeError, ValueError) as error:
            get_pointer = ctypes.pythonapi.PyCapsule_GetPointer
            get_pointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
            get_pointer.restype = ctypes.c_void_p
            pointer = get_pointer(message, None)
            if not pointer:
                raise ValueError("原生消息指针为空") from error
            return int(pointer)

        if not pointer:
            raise ValueError("原生消息指针为空")
        return pointer
