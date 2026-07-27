"""LinguaFlow quick-translation popup window."""

from __future__ import annotations

import logging

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from core.logger import get_logger
from ui.components.lf_button import LFButton
from ui.components.lf_card import LFCard
from ui.resources.assets import get_logo
from ui.theme.theme import COLORS, RADIUS, SPACING


class PopupWindow(QWidget):
    """Display quick translation feedback without taking focus."""

    HIDE_DELAY_MS = 3000
    DEFAULT_WIDTH = 420
    MIN_WIDTH = 280
    MAX_WIDTH = 600
    RIGHT_MARGIN = SPACING.xl + SPACING.sm
    BOTTOM_MARGIN = SPACING.xl * 2
    MARGIN = RIGHT_MARGIN

    retry_requested = Signal()

    def __init__(self, logger: logging.Logger | None = None) -> None:
        super().__init__()
        self._logger = logger or get_logger(__name__)
        self._source_text = ""
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._hide_popup)
        self._build_ui()

    def show_result(self, text: str, source_text: str = "") -> None:
        """Display a translation result and start the auto-hide timer."""
        self._source_text = source_text
        self.source_label.setText(source_text)
        self.source_label.setVisible(bool(source_text))
        self.result_label.setText(text)
        self.adjustSize()
        self.setFixedWidth(self._clamp_width(self.width()))
        self.adjustSize()
        self._move_to_bottom_right()
        self.hide_timer.start(self.HIDE_DELAY_MS)
        self.show()
        self._logger.info("Popup shown")

    def _build_ui(self) -> None:
        self.setObjectName("PopupWindow")
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMaximumWidth(self.MAX_WIDTH)
        self.resize(self.DEFAULT_WIDTH, 160)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        self.card = LFCard(self)
        card_layout = self.card.layout()
        if card_layout is None:
            raise RuntimeError("Popup card layout is missing")
        outer_layout.addWidget(self.card)

        card_layout.setSpacing(SPACING.md)
        card_layout.addWidget(self._build_header())
        card_layout.addWidget(self._build_content())
        card_layout.addWidget(self._build_actions())
        self.setStyleSheet(f"""
            QWidget#PopupWindow {{
                background-color: {COLORS.surface};
                border-radius: {RADIUS.card}px;
            }}
            QLabel#PopupSource {{
                color: {COLORS.secondary_text};
                font-size: 12px;
            }}
            QLabel#PopupResult {{
                color: {COLORS.text};
                font-size: 15px;
            }}
            """)

    def _build_header(self) -> QWidget:
        header = QWidget(self)
        header.setFixedHeight(40)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        logo = QLabel(header)
        logo.setPixmap(QPixmap(str(get_logo(16))))
        logo.setFixedSize(16, 16)
        self.logo_label = logo
        layout.addWidget(logo)
        title = QLabel("LinguaFlow", header)
        title.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        layout.addWidget(title)
        layout.addStretch()
        self.close_button = LFButton("×", variant="ghost")
        self.close_button.setFixedSize(32, 32)
        self.close_button.clicked.connect(self._hide_popup)
        layout.addWidget(self.close_button)
        return header

    def _build_content(self) -> QWidget:
        content = QWidget(self)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING.sm)
        self.source_label = QLabel(content)
        self.source_label.setObjectName("PopupSource")
        self.source_label.setWordWrap(True)
        self.source_label.setMaximumHeight(80)
        self.source_label.setVisible(False)
        layout.addWidget(self.source_label)
        self.result_label = QLabel(content)
        self.result_label.setObjectName("PopupResult")
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.result_label)
        self.label = self.result_label
        return content

    def _build_actions(self) -> QWidget:
        actions = QWidget(self)
        layout = QHBoxLayout(actions)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        self.copy_button = LFButton("Copy", variant="secondary")
        self.copy_button.clicked.connect(self._copy_result)
        self.retry_button = LFButton("Retry", variant="secondary")
        self.retry_button.clicked.connect(self.retry_requested.emit)
        self.dismiss_button = LFButton("Close", variant="ghost")
        self.dismiss_button.clicked.connect(self._hide_popup)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.retry_button)
        layout.addWidget(self.dismiss_button)
        return actions

    def _copy_result(self) -> None:
        QApplication.clipboard().setText(self.result_label.text())
        self._logger.info("Popup result copied")

    def _move_to_bottom_right(self) -> None:
        """Move the popup to the bottom-right of the available screen area."""
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        available_geometry = screen.availableGeometry()
        x = available_geometry.right() - self.width() - self.RIGHT_MARGIN
        y = available_geometry.bottom() - self.height() - self.BOTTOM_MARGIN
        self.move(x, y)

    def _clamp_width(self, width: int) -> int:
        return max(self.MIN_WIDTH, min(self.MAX_WIDTH, max(self.DEFAULT_WIDTH, width)))

    def enterEvent(self, event: object | None) -> None:
        """Pause auto-hide while the pointer is over the popup."""
        self.hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event: object | None) -> None:
        """Resume auto-hide after the pointer leaves the popup."""
        self.hide_timer.start(self.HIDE_DELAY_MS)
        super().leaveEvent(event)

    def _hide_popup(self) -> None:
        self.hide()
        self._logger.info("Popup hidden")
