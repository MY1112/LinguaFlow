"""Settings Selection page."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QLabel

from ui.components.lf_card import LFCard
from ui.theme.theme import COLORS


class SelectionPage(LFCard):
    """展示划词翻译相关设置的页面骨架。"""

    def __init__(self, config_service=None) -> None:
        super().__init__(padding=24)
        self.title_label = QLabel("Selection", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        self.selection_translation_check = QCheckBox("Enable selection translation", self)
        self.selection_translation_check.setChecked(True)
        self.show_popup_check = QCheckBox("Show Popup when translation completes", self)
        self.show_popup_check.setChecked(True)
        self.default_behavior_label = QLabel("Default behavior: Translate selected text", self)
        self.default_behavior_label.setStyleSheet(
            f"color: {COLORS.secondary_text}; font-size: 14px;"
        )
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.selection_translation_check)
        self.layout().addWidget(self.show_popup_check)
        self.layout().addWidget(self.default_behavior_label)
        self.layout().addStretch()
