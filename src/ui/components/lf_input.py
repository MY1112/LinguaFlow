"""LinguaFlow 统一文本输入组件。"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QLabel, QPlainTextEdit

from ui.theme.theme import COLORS, RADIUS, SPACING


class LFInput(QPlainTextEdit):
    """提供统一样式、最大长度限制，内置右下角字符统计标签的多行文本输入框。

    Args:
        max_length: 文本最大长度
        has_border: 是否显示边框
        show_count: 是否启用右下角字符统计
    """

    def __init__(
        self,
        max_length: int = 5000,
        has_border: bool = True,
        show_count: bool = True,
    ) -> None:
        super().__init__()
        self.maximum_length = max_length
        self.has_border = has_border
        self.padding = SPACING.sm
        self.show_count = show_count
        self._enforcing_length = False

        # 内置字符计数标签
        self.count_label = QLabel(self)
        self.count_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.count_label.setStyleSheet(f"""
            color: {COLORS.secondary_text};
            font-size: 12px;
        """)
        self.count_label.setVisible(self.show_count)

        self._build_stylesheet()
        # self.textChanged.connect(self._enforce_maximum_length)
        self.textChanged.connect(self._update_count_text)
        self._update_count_text()

    def _build_stylesheet(self):
        """动态构建样式表"""
        if self.has_border:
            border_style = f"1px solid {COLORS.border}"
            focus_border_color = COLORS.primary
        else:
            border_style = "none"
            focus_border_color = "transparent"

        if self.padding is None:
            padding_css = "padding: 0px;"
            pad_val = 0
        else:
            padding_css = f"padding: {self.padding}px;"
            pad_val = self.padding

        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS.surface};
                color: {COLORS.text};
                border: {border_style};
                border-radius: {RADIUS.large}px;
                {padding_css}
                font-size: 14px;
            }}
            QPlainTextEdit:focus {{
                border-color: {focus_border_color};
            }}
            """)
        # 缓存padding数值，用于标签定位
        self._pad_value = pad_val
        self._update_label_position()

    def _update_count_text(self):
        """更新字符计数：当前 / 上限"""
        current_len = len(self.toPlainText())
        self.count_label.setText(f"{current_len} / {self.maximum_length}")
        self.count_label.adjustSize()
        self._update_label_position()

    def _update_label_position(self):
        """将标签固定至右下角，留出内边距偏移"""
        if not self.show_count:
            return
        margin = self._pad_value + 4
        label_w = self.count_label.sizeHint().width()
        label_h = self.count_label.sizeHint().height()
        x = self.width() - label_w - margin
        y = self.height() - label_h - margin
        self.count_label.move(x, y)
        self.count_label.raise_()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._update_label_position()

    def set_has_border(self, enable: bool):
        if self.has_border == enable:
            return
        self.has_border = enable
        self._build_stylesheet()

    def set_padding(self, value: int | None):
        if self.padding == value:
            return
        self.padding = value
        self._build_stylesheet()

    def set_show_count(self, visible: bool):
        """动态开启/关闭字符统计显示"""
        self.show_count = visible
        self.count_label.setVisible(visible)
        if visible:
            self._update_label_position()

    def setPlainText(self, text: str) -> None:
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
