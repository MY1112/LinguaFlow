"""LinguaFlow branded MainWindow header component."""

from __future__ import annotations

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt

from ui.resources.assets import get_logo
from ui.theme.theme import COLORS, SPACING


class LFHeader(QWidget):
    """Display the approved logo, product name and subtitle."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(72)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING.md - SPACING.xs)

        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap(str(get_logo(32))))
        self.logo_label.setFixedSize(32, 32)
        layout.addWidget(self.logo_label)

        brand_layout = QVBoxLayout()
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(0)
        self.title_label = QLabel("LinguaFlow", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        self.title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.subtitle_label = QLabel("Translate Naturally.", self)
        self.subtitle_label.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 12px;")
        self.subtitle_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        brand_layout.addWidget(self.title_label)
        brand_layout.addWidget(self.subtitle_label)
        layout.addLayout(brand_layout)
        layout.addStretch()
