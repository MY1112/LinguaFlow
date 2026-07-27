"""LinguaFlow 统一状态展示组件。"""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from ui.theme.theme import COLORS, SPACING


class LFStatus(QWidget):
    """显示状态圆点和状态文案。"""

    _COLORS = {
        "success": COLORS.success,
        "loading": COLORS.primary,
        "error": COLORS.error,
    }

    def __init__(self, text: str, variant: str = "success") -> None:
        if variant not in self._COLORS:
            raise ValueError(f"不支持的状态类型：{variant}")
        super().__init__()
        self.text = text
        self.variant = variant
        self.dot = QLabel("●")
        self.label = QLabel(text)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING.xs)
        layout.addWidget(self.dot)
        layout.addWidget(self.label)
        layout.addStretch()
        self._apply_style()

    def set_status(self, text: str, variant: str) -> None:
        """更新状态文案和类型。"""
        if variant not in self._COLORS:
            raise ValueError(f"不支持的状态类型：{variant}")
        self.text = text
        self.variant = variant
        self.label.setText(text)
        self._apply_style()

    def _apply_style(self) -> None:
        self.dot.setStyleSheet(f"color: {self._COLORS[self.variant]};")
        self.label.setStyleSheet(f"color: {COLORS.text}; font-size: 12px;")
