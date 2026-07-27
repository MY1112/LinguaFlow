"""LinguaFlow 统一按钮组件。"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from ui.theme.theme import COLORS, RADIUS


class LFButton(QPushButton):
    """提供统一尺寸和变体样式的按钮。"""

    _VARIANTS = {"primary", "secondary", "danger", "ghost"}

    def __init__(self, text: str = "", variant: str = "primary") -> None:
        if variant not in self._VARIANTS:
            raise ValueError(f"不支持的按钮类型：{variant}")
        super().__init__(text)
        self.variant = variant
        self.setMinimumHeight(42)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()

    def _apply_style(self) -> None:
        background, foreground, border = {
            "primary": (COLORS.primary, COLORS.surface, COLORS.primary),
            "secondary": (COLORS.surface, COLORS.text, COLORS.border),
            "danger": (COLORS.error, COLORS.surface, COLORS.error),
            "ghost": ("transparent", COLORS.text, "transparent"),
        }[self.variant]
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {background};
                color: {foreground};
                border: 1px solid {border};
                border-radius: {RADIUS.pill}px;
                padding: 0 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                border-color: {COLORS.primary};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
            """)
