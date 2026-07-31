"""LinguaFlow Settings window."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from services.config_service import ConfigService
from ui.components.lf_button import LFButton
from ui.settings.pages.about_page import AboutPage
from ui.settings.pages.general_page import GeneralPage
from ui.settings.pages.model_page import ModelPage
from ui.settings.pages.ocr_page import OcrPage
from ui.settings.pages.selection_page import SelectionPage
from ui.settings.pages.shortcut_page import ShortcutPage
from ui.theme.theme import COLORS, RADIUS, SPACING


class SettingsWindow(QWidget):
    """提供 Settings 信息架构与页面切换。"""

    PAGE_TYPES = (
        ("general", "通用", GeneralPage),
        ("selection", "划词", SelectionPage),
        ("model", "模型", ModelPage),
        ("shortcut", "快捷键", ShortcutPage),
        ("ocr", "OCR", OcrPage),
        ("about", "关于", AboutPage),
    )

    def __init__(self, config_service: ConfigService | None = None) -> None:
        super().__init__()
        self.setObjectName("SettingsWindow")
        self.setWindowTitle("设置")
        self.resize(720, 520)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowMinimizeButtonHint
        )
        self.setFixedSize(720, 520)
        self.setStyleSheet(f"QWidget#SettingsWindow {{ background-color: {COLORS.background}; }}")
        self.config_service = config_service
        self._current_page = "general"
        self._build_ui()

    @property
    def current_page(self) -> str:
        """返回当前选中的页面 key。"""
        return self._current_page

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(SPACING.lg, SPACING.lg, SPACING.lg, SPACING.lg)
        root_layout.setSpacing(SPACING.md)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(SPACING.md)
        self.sidebar = self._build_sidebar()
        body_layout.addWidget(self.sidebar)
        self.content_area = self._build_content_area()
        body_layout.addWidget(self.content_area, 1)
        root_layout.addLayout(body_layout, 1)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(160)
        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS.surface};
                border-radius: {RADIUS.card}px;
                border:1px solid {COLORS.border};
            }}
            """)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(SPACING.sm, SPACING.sm, SPACING.sm, SPACING.sm)
        layout.setSpacing(SPACING.xs)
        self.sidebar_buttons: dict[str, LFButton] = {}
        for page_key, label, _ in self.PAGE_TYPES:
            button = LFButton(label, variant="ghost")
            button.setObjectName(f"{page_key}_button")
            button.setCheckable(True)
            button.setMinimumHeight(40)

            def make_callback(k):
                return lambda checked=False: self.select_page(k)

            button.clicked.connect(make_callback(page_key))
            self.sidebar_buttons[page_key] = button
            layout.addWidget(button)
        layout.addStretch()
        return sidebar

    def _build_content_area(self) -> QStackedWidget:
        self.page_stack = QStackedWidget(self)
        self.page_stack.setObjectName("content_area")
        self.pages: dict[str, QWidget] = {}
        for page_key, _, page_type in self.PAGE_TYPES:
            page = page_type(self.config_service)
            self.pages[page_key] = page
            self.page_stack.addWidget(page)
        self.select_page(self._current_page)
        return self.page_stack

    def select_page(self, page_key: str) -> None:
        """按稳定 key 选择 Settings 页面。"""
        if page_key not in self.pages:
            raise ValueError(f"Unknown settings page: {page_key}")
        self._current_page = page_key
        self.page_stack.setCurrentWidget(self.pages[page_key])
        for key, button in self.sidebar_buttons.items():
            button.setChecked(key == page_key)
