"""PopupWindow 的行为测试。"""

from __future__ import annotations

import logging

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ui.popup_window import PopupWindow


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    """提供 Qt 测试应用实例。"""
    return QApplication.instance() or QApplication([])


def test_show_result_displays_text_without_activation(qt_application: QApplication) -> None:
    """show_result 应显示文本并保持窗口不抢焦点。"""
    popup = PopupWindow(logging.getLogger("test.popup"))

    popup.show_result("翻译结果")
    qt_application.processEvents()

    assert popup.label.text() == "翻译结果"
    assert popup.isVisible()
    assert popup.focusPolicy() == Qt.FocusPolicy.NoFocus
    assert popup.testAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    popup.close()


def test_popup_window_uses_non_taskbar_topmost_frameless_flags(
    qt_application: QApplication,
) -> None:
    """PopupWindow 应使用无边框、置顶且不进入任务栏的窗口标志。"""
    popup = PopupWindow(logging.getLogger("test.popup"))
    flags = popup.windowFlags()

    assert flags & Qt.WindowType.FramelessWindowHint
    assert flags & Qt.WindowType.WindowStaysOnTopHint
    assert flags & Qt.WindowType.Tool
    assert flags & Qt.WindowType.WindowDoesNotAcceptFocus

    popup.close()


def test_show_result_places_popup_at_screen_bottom_right(
    qt_application: QApplication,
) -> None:
    """show_result 应把窗口放在主屏幕可用区域右下角。"""
    popup = PopupWindow(logging.getLogger("test.popup"))

    popup.show_result("结果")
    qt_application.processEvents()

    available_geometry = qt_application.primaryScreen().availableGeometry()
    expected_x = available_geometry.right() - popup.width() - popup.MARGIN
    expected_y = available_geometry.bottom() - popup.height() - popup.MARGIN

    assert popup.x() == expected_x
    assert popup.y() == expected_y

    popup.close()


def test_show_result_starts_auto_hide_timer(qt_application: QApplication) -> None:
    """show_result 应启动自动隐藏计时器。"""
    popup = PopupWindow(logging.getLogger("test.popup"))

    popup.show_result("结果")

    assert popup.hide_timer.isActive()
    assert popup.hide_timer.interval() == popup.HIDE_DELAY_MS

    popup.close()
