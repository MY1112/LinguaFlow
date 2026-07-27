"""LinguaFlow language selector component."""

from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtWidgets import QComboBox, QWidget

from ui.theme.theme import COLORS, RADIUS


class LFSelect(QComboBox):
    """Provide the shared selector dimensions and visual style."""

    def __init__(
        self,
        items: Iterable[str] = (),
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.addItems(list(items))
        self.setFixedSize(152, 40)
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS.surface};
                color: {COLORS.text};
                border: 1px solid {COLORS.border};
                border-radius: {RADIUS.large}px;
                padding: 0 12px;
                font-size: 14px;
            }}
            QComboBox:hover, QComboBox:focus {{
                border-color: {COLORS.primary};
            }}
            """)
