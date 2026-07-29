"""LinguaFlow shared card component."""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QWidget

from ui.theme.theme import COLORS, RADIUS, SPACING


class LFCard(QFrame):
    """Provide the shared card surface, padding, radius and shadow."""

    def __init__(self, parent: QWidget | None = None, padding: int | None = SPACING.md) -> None:
        super().__init__(parent)
        self.setObjectName("LFCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(padding, padding, padding, padding)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow_color = QColor(COLORS.text)
        shadow_color.setAlpha(13)
        shadow.setColor(shadow_color)
        self.setGraphicsEffect(shadow)
        self.setStyleSheet(f"""
            QFrame#LFCard {{
                background-color: {COLORS.surface};
                border: 1px solid {COLORS.border};
                border-radius: {RADIUS.card}px;
            }}
            """)
