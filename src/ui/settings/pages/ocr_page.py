"""Settings OCR page."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QLabel

from ui.components.lf_card import LFCard
from ui.theme.theme import COLORS


class OcrPage(LFCard):
    """展示 OCR 设置占位内容的页面。"""

    def __init__(self, config_service=None) -> None:
        super().__init__(padding=24)
        self.title_label = QLabel("OCR", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        self.ocr_enabled_check = QCheckBox("Enable OCR", self)
        self.ocr_enabled_check.setChecked(False)
        self.ocr_shortcut_label = QLabel("OCR shortcut: Not configured", self)
        self.ocr_language_label = QLabel("OCR language: Chinese / English (placeholder)", self)
        for label in (self.ocr_shortcut_label, self.ocr_language_label):
            label.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.ocr_enabled_check)
        self.layout().addWidget(self.ocr_shortcut_label)
        self.layout().addWidget(self.ocr_language_label)
        self.layout().addStretch()
