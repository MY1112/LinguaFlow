"""SettingsWindow 基础结构测试。"""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication

from ui.settings.pages.about_page import AboutPage
from ui.settings.pages.general_page import GeneralPage
from ui.settings.pages.model_page import ModelPage
from ui.settings.pages.ocr_page import OcrPage
from ui.settings.pages.selection_page import SelectionPage
from ui.settings.pages.shortcut_page import ShortcutPage
from ui.settings.settings_window import SettingsWindow


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_settings_window_has_information_architecture(
    qt_application: QApplication,
) -> None:
    window = SettingsWindow()

    assert window.size().width() == 720
    assert window.size().height() == 520
    assert window.sidebar is not None
    assert window.content_area is not None
    assert list(window.pages) == ["general", "selection", "model", "shortcut", "ocr", "about"]
    assert isinstance(window.pages["general"], GeneralPage)
    assert isinstance(window.pages["selection"], SelectionPage)
    assert isinstance(window.pages["model"], ModelPage)
    assert isinstance(window.pages["shortcut"], ShortcutPage)
    assert isinstance(window.pages["ocr"], OcrPage)
    assert isinstance(window.pages["about"], AboutPage)

    window.close()


def test_settings_sidebar_switches_content_page(qt_application: QApplication) -> None:
    window = SettingsWindow()

    assert window.current_page == "general"

    for page_key in ("model", "selection", "ocr"):
        window.select_page(page_key)
        assert window.current_page == page_key
        assert window.page_stack.currentWidget() is window.pages[page_key]

    window.close()
