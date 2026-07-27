"""M4-004 MainWindow layout tests."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication

from ui.components.lf_header import LFHeader
from ui.components.lf_select import LFSelect
from ui.main_window import MainWindow


class FakeTranslationFeature:
    """Prevent MainWindow tests from invoking a real model."""


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    """Provide a Qt application for widget tests."""
    return QApplication.instance() or QApplication([])


def test_header_component_uses_brand_assets(qt_application: QApplication) -> None:
    """LFHeader should expose the approved logo and brand text."""
    header = LFHeader()

    assert header.logo_label.pixmap() is not None
    assert header.title_label.text() == "LinguaFlow"
    assert header.subtitle_label.text() == "Translate Naturally."
    assert header.height() == 72

    header.close()


def test_select_component_has_design_dimensions(qt_application: QApplication) -> None:
    """LFSelect should provide the styled language selector component."""
    select = LFSelect(["中文", "English"])

    assert select.count() == 2
    assert select.width() == 152
    assert select.height() == 40

    select.close()


def test_main_window_uses_m4004_layout(qt_application: QApplication) -> None:
    """MainWindow should match the implementation reference dimensions."""
    window = MainWindow(FakeTranslationFeature())

    assert window.size().width() == 420
    assert window.size().height() == 620
    assert isinstance(window.header, LFHeader)
    assert isinstance(window.source_language, LFSelect)
    assert isinstance(window.target_language, LFSelect)
    assert window.input_card.width() == 372
    assert window.result_card.width() == 372
    assert window.translate_button.width() == 240
    assert window.translate_button.height() == 44
    assert window.copy_button.text() == "Copy"
    assert window.sound_button.text() == "Sound"
    assert window._get_translation_direction() == ("中文", "English")

    window.close()
