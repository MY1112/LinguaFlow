"""LinguaFlow 统一文本输入组件。"""

from __future__ import annotations

from PySide6.QtWidgets import QPlainTextEdit

from ui.theme.theme import COLORS, RADIUS, SPACING


class LFInput(QPlainTextEdit):
    """提供统一样式和最大长度限制的多行文本输入框。"""

    def __init__(self, max_length: int = 5000) -> None:
        super().__init__()
        self.maximum_length = max_length
        self._enforcing_length = False
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS.surface};
                color: {COLORS.text};
                border: 1px solid {COLORS.border};
                border-radius: {RADIUS.large}px;
                padding: {SPACING.sm}px;
                font-size: 14px;
            }}
            QPlainTextEdit:focus {{
                border-color: {COLORS.primary};
            }}
            """)
        self.textChanged.connect(self._enforce_maximum_length)

    def setPlainText(self, text: str) -> None:
        """设置文本并遵守最大长度限制。"""
        super().setPlainText(text[: self.maximum_length])

    def _enforce_maximum_length(self) -> None:
        if self._enforcing_length:
            return
        text = self.toPlainText()
        if len(text) <= self.maximum_length:
            return
        self._enforcing_length = True
        self.setPlainText(text[: self.maximum_length])
        self._enforcing_length = False
