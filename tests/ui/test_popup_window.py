"""PopupWindow behavior tests."""

from __future__ import annotations

import logging

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ui.popup_window import PopupWindow


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    """Provide a Qt application for widget tests."""
    return QApplication.instance() or QApplication([])


def test_show_result_displays_text_without_activation(qt_application: QApplication) -> None:
    """show_result displays text without taking focus."""
    popup = PopupWindow(logging.getLogger("test.popup"))

    popup.show_result("translated result")
    qt_application.processEvents()

    assert popup.label.text() == "translated result"
    assert popup.isVisible()
    assert popup.focusPolicy() == Qt.FocusPolicy.NoFocus
    assert popup.testAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    popup.close()


def test_popup_window_uses_non_taskbar_topmost_frameless_flags(
    qt_application: QApplication,
) -> None:
    """Popup uses frameless, topmost and non-taskbar flags."""
    popup = PopupWindow(logging.getLogger("test.popup"))
    flags = popup.windowFlags()

    assert flags & Qt.WindowType.FramelessWindowHint
    assert flags & Qt.WindowType.WindowStaysOnTopHint
    assert flags & Qt.WindowType.Tool
    assert flags & Qt.WindowType.WindowDoesNotAcceptFocus

    popup.close()


def test_show_result_places_popup_at_specified_screen_margins(
    qt_application: QApplication,
) -> None:
    """show_result places Popup at the specified bottom-right margins."""
    popup = PopupWindow(logging.getLogger("test.popup"))

    popup.show_result("result")
    qt_application.processEvents()

    available_geometry = qt_application.primaryScreen().availableGeometry()
    expected_x = available_geometry.right() - popup.width() - popup.RIGHT_MARGIN
    expected_y = available_geometry.bottom() - popup.height() - popup.BOTTOM_MARGIN

    assert popup.x() == expected_x
    assert popup.y() == expected_y

    popup.close()


def test_show_result_starts_auto_hide_timer(qt_application: QApplication) -> None:
    """show_result starts the three-second auto-hide timer."""
    popup = PopupWindow(logging.getLogger("test.popup"))

    popup.show_result("result")

    assert popup.hide_timer.isActive()
    assert popup.hide_timer.interval() == popup.HIDE_DELAY_MS
    assert popup.HIDE_DELAY_MS == 5000

    popup.close()
