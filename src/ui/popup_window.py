"""用于显示翻译结果的悬浮窗口。"""

from __future__ import annotations

import logging

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from core.logger import get_logger


class PopupWindow(QWidget):
    """只负责显示文本的右下角悬浮窗口。"""

    MARGIN = 24
    HIDE_DELAY_MS = 3000

    def __init__(self, logger: logging.Logger | None = None) -> None:
        super().__init__()
        self._logger = logger or get_logger(__name__)
        self.label = QLabel(self)
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._hide_popup)
        self._build_ui()

    def show_result(self, text: str) -> None:
        """显示文本并在固定时间后自动隐藏。"""
        self.label.setText(text)
        self.adjustSize()
        self._move_to_bottom_right()
        self.hide_timer.start(self.HIDE_DELAY_MS)
        self.show()
        self._logger.info("Popup 显示")

    def _build_ui(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.addWidget(self.label)

    def _move_to_bottom_right(self) -> None:
        """将窗口放到主屏幕可用区域右下角。"""
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        available_geometry = screen.availableGeometry()
        x = available_geometry.right() - self.width() - self.MARGIN
        y = available_geometry.bottom() - self.height() - self.MARGIN
        self.move(x, y)

    def _hide_popup(self) -> None:
        self.hide()
        self._logger.info("Popup 隐藏")
