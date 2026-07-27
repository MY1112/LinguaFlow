"""PopupWindow 产品化重构测试。"""

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


def test_popup_matches_product_structure_and_dimensions(
    qt_application: QApplication,
) -> None:
    """Popup 应包含规范要求的 Header、内容区和操作区。"""
    popup = PopupWindow(logging.getLogger("test.popup.refactor"))

    assert popup.width() == 420
    assert popup.minimumWidth() == 280
    assert popup.maximumWidth() == 600
    assert popup.logo_label.pixmap() is not None
    assert popup.close_button is not None
    assert popup.source_label is not None
    assert popup.result_label is popup.label
    assert popup.copy_button is not None
    assert popup.retry_button is not None
    assert popup.dismiss_button is not None
    assert popup.windowFlags() & Qt.WindowType.WindowDoesNotAcceptFocus

    popup.close()


def test_show_result_updates_content_and_starts_auto_hide_timer(
    qt_application: QApplication,
) -> None:
    """show_result 应更新译文、显示窗口并启动 3 秒自动隐藏。"""
    popup = PopupWindow(logging.getLogger("test.popup.refactor"))

    popup.show_result("translated text")

    assert popup.result_label.text() == "translated text"
    assert popup.isVisible()
    assert popup.hide_timer.isActive()
    assert popup.hide_timer.interval() == 3000

    popup.close()


def test_popup_pauses_and_resumes_auto_hide_on_mouse_presence(
    qt_application: QApplication,
) -> None:
    """鼠标进入 Popup 时暂停自动隐藏，离开后恢复计时。"""
    popup = PopupWindow(logging.getLogger("test.popup.refactor"))
    popup.show_result("translated text")

    popup.enterEvent(None)
    assert not popup.hide_timer.isActive()

    popup.leaveEvent(None)
    assert popup.hide_timer.isActive()

    popup.close()
