"""LinguaFlow 统一卡片容器。"""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from ui.theme.theme import COLORS, RADIUS, SPACING


class LFCard(QFrame):
    """提供统一背景、圆角和内边距的卡片容器。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("LFCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING.lg - SPACING.xs,
            SPACING.lg - SPACING.xs,
            SPACING.lg - SPACING.xs,
            SPACING.lg - SPACING.xs,
        )
        self.setStyleSheet(f"""
            QFrame#LFCard {{
                background-color: {COLORS.surface};
                border: 1px solid {COLORS.border};
                border-radius: {RADIUS.card}px;
            }}
            """)
