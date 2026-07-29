"""MainWindow product layout tests."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


class FakeTranslationFeature:
    """Prevent MainWindow tests from invoking a real model."""


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    """Provide a Qt application for widget tests."""
    return QApplication.instance() or QApplication([])


def test_main_window_matches_product_layout(qt_application: QApplication) -> None:
    """MainWindow should expose the required content areas."""
    window = MainWindow(FakeTranslationFeature())

    assert window.windowTitle() == "LinguaFlow"
    assert window.size().width() == 420
    assert window.size().height() == 620
    assert window.minimumSize().width() == 420
    assert window.minimumSize().height() == 520
    assert window.logo_label.pixmap() is not None
    assert window.source_language.currentText() == "中文"
    assert window.target_language.currentText() == "English"
    assert window.source_text_edit.maximum_length == 5000
    assert window.source_text_edit.parent() is window.input_card
    assert window.translate_button.text() == "Translate"
    assert window.result_title.text() == "Translation Result"
    assert window.model_status.text == "Model Ready"

    window.close()


def test_main_window_swaps_languages_and_keeps_direction_api(
    qt_application: QApplication,
) -> None:
    """The swap button should preserve the existing direction API."""
    window = MainWindow(FakeTranslationFeature())

    assert window._get_translation_direction() == ("中文", "English")
    window.swap_button.click()

    assert window._get_translation_direction() == ("English", "中文")
    assert window.source_language.currentText() == "English"
    assert window.target_language.currentText() == "中文"

    window.close()


def test_main_window_updates_character_count(qt_application: QApplication) -> None:
    """Typing text should update the character counter."""
    window = MainWindow(FakeTranslationFeature())

    window.source_text_edit.setPlainText("hello")

    assert window.source_text_edit.count_label.text() == "5 / 5000"
    window.close()
