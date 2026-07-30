"""Application 划词翻译协调流程测试。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from app.application import Application


class _SelectionAdapter:
    def __init__(self) -> None:
        self.foreground_hwnd: int | None = None

    def capture_selected_text(self, foreground_hwnd: int | None = None) -> bool:
        self.foreground_hwnd = foreground_hwnd
        return True


def _create_application() -> Application:
    application = Application.__new__(Application)
    application.selection_adapter = _SelectionAdapter()
    application.context = SimpleNamespace(logger=Mock())
    application._start_selection_translation = Mock()
    return application


def test_translation_requests_async_selection_capture() -> None:
    """热键流程应异步请求 SelectionAdapter 捕获文本。"""
    application = _create_application()

    application._translate_selection(1234)

    assert application.selection_adapter.foreground_hwnd == 1234


def test_empty_selection_ends_without_starting_translation() -> None:
    """没有选中文本时不应启动 Worker。"""
    application = _create_application()

    application._on_selection_captured("")

    application._start_selection_translation.assert_not_called()
    application.context.logger.info.assert_called()


def test_selection_starts_translation_with_selected_text() -> None:
    """获取到选中文本时应交给 Application 启动后台翻译。"""
    application = _create_application()

    application._on_selection_captured("Hello")

    application._start_selection_translation.assert_called_once_with("Hello")


def test_translation_failure_shows_generic_popup_and_logs_detail() -> None:
    """翻译失败时 Popup 只显示通用提示，日志保留详细错误。"""
    application = Application.__new__(Application)
    application.popup_window = Mock()
    application.context = SimpleNamespace(logger=Mock())

    application._on_selection_translation_failed("模型未加载")

    application.popup_window.show_error.assert_called_once_with("翻译失败")
    application.context.logger.error.assert_called_once()


def test_translation_success_shows_result_in_popup() -> None:
    """翻译成功时应将结果交给 PopupWindow。"""
    application = Application.__new__(Application)
    application.popup_window = Mock()
    application.context = SimpleNamespace(logger=Mock())

    application._on_selection_translation_finished("Hello")

    application.popup_window.show_result.assert_called_once_with("Hello")


def test_translation_success_passes_source_text_to_popup() -> None:
    """Selection translation should show the selected source alongside its result."""
    application = Application.__new__(Application)
    application.popup_window = Mock()
    application.context = SimpleNamespace(logger=Mock())
    application._selection_source_text = "Hello"

    application._on_selection_translation_finished("你好")

    application.popup_window.show_result.assert_called_once_with("你好", "Hello")


def test_retry_restarts_translation_with_previous_source() -> None:
    """Retry should submit the same selected text again."""
    application = Application.__new__(Application)
    application._selection_source_text = "Hello"
    application._start_selection_translation = Mock()

    application._retry_selection_translation()

    application._start_selection_translation.assert_called_once_with("Hello")
