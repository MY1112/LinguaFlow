"""M4-005 visual calibration tests."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect

from ui.components.lf_button import LFButton
from ui.components.lf_card import LFCard
from ui.main_window import MainWindow


class FakeTranslationFeature:
    """Prevent visual tests from invoking a real model."""


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    """Provide a Qt application for widget tests."""
    return QApplication.instance() or QApplication([])


def test_button_uses_standard_visual_radius(qt_application: QApplication) -> None:
    """Buttons should use the 12px implementation-spec radius."""
    button = LFButton("Translate")

    assert "border-radius: 12px" in button.styleSheet()

    button.close()


def test_card_uses_design_padding_and_soft_shadow(qt_application: QApplication) -> None:
    """Cards should use the approved 16px padding and soft shadow."""
    card = LFCard()
    margins = card.layout().contentsMargins()

    assert margins.left() == 16
    assert margins.top() == 16
    assert isinstance(card.graphicsEffect(), QGraphicsDropShadowEffect)
    assert card.graphicsEffect().blurRadius() == 16

    card.close()


def test_main_window_uses_result_title_typography(qt_application: QApplication) -> None:
    """MainWindow result heading should use the section-title hierarchy."""
    window = MainWindow(FakeTranslationFeature())
    assert "font-size: 15px" in window.result_title.styleSheet()

    window.close()
