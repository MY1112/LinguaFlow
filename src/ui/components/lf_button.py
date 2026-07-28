"""LinguaFlow shared button component."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from ui.theme.theme import COLORS, RADIUS


class LFButton(QPushButton):
    """Provide shared button dimensions and visual variants.
    Supports text only, icon only, icon + text.
    """

    _VARIANTS = {"primary", "secondary", "danger", "ghost"}

    def __init__(
        self,
        text: str = "",
        variant: str = "primary",
        icon_path: str | Path | None = None,
        icon_size: tuple[int, int] = (16, 16),
    ) -> None:
        if variant not in self._VARIANTS:
            raise ValueError(f"Unsupported button variant: {variant}")
        super().__init__(text)
        self.variant = variant
        self.setMinimumHeight(42)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 图标设置
        if icon_path is not None:
            self.setIcon(QIcon(str(icon_path)))
            self.setIconSize(QSize(*icon_size))

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
                border-radius: {RADIUS.large}px;
                padding: 0 20px;
                font-size: 14px;
                font-family: "Segoe UI", "Microsoft YaHei", system-ui, sans-serif;
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {COLORS.primary};
            }}
            /* ghost 增加悬浮背景，提升体验 */
            QPushButton:ghost:hover {{
                background: rgba(128,128,128,0.08);
            }}
            QPushButton:disabled {{
                color: rgba(120,120,120,0.45);
            }}
        """)
