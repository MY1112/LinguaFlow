"""LinguaFlow quick-translation popup window."""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.logger import get_logger
from ui.components.lf_button import LFButton
from ui.components.lf_card import LFCard
from ui.components.lf_icon_label import LFIconLabel
from ui.resources.assets import get_icon, get_logo
from ui.theme.theme import COLORS, RADIUS, SPACING


class PopupWindow(QWidget):
    """Display quick translation feedback without taking focus."""

    MAX_SCROLL_H = 240
    HIDE_DELAY_MS = 5000
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
        source_visible = bool(source_text.strip())

        self.source_label.setVisible(source_visible)
        self.source_row.setVisible(source_visible)

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
        self.card = LFCard(self, padding=0)
        card_layout = self.card.layout()
        if card_layout is None:
            raise RuntimeError("Popup card layout is missing")
        outer_layout.addWidget(self.card)

        card_layout.setSpacing(SPACING.md)
        self.header = self._build_header()
        card_layout.addWidget(self.header)
        self.content = self._build_content()
        card_layout.addWidget(self.content)
        self.actions = self._build_actions()
        card_layout.addWidget(self.actions)
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
        header.setStyleSheet(f"""
            QWidget{{
                background-color: {COLORS.background};
                border-top-left-radius: {RADIUS.card}px;
                border-top-right-radius: {RADIUS.card}px;
            }}
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(12, 0, 12, 0)
        logo = QLabel(header)
        logo.setPixmap(QPixmap(str(get_logo(16))))
        logo.setFixedSize(16, 16)
        self.logo_label = logo
        layout.addWidget(logo)
        title = QLabel("Translation", header)
        title.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        layout.addWidget(title)
        layout.addStretch()
        self.close_button = LFIconLabel(header)
        close_pix = QPixmap(str(get_icon("close")))
        self.close_button.setPixmap(
            close_pix.scaled(
                16,
                16,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.close_button.setFixedSize(16, 16)
        self.close_button.clicked.connect(self._hide_popup)
        layout.addWidget(self.close_button)
        return header

    def _build_content(self) -> QWidget:
        content = QWidget(self)
        content.setStyleSheet(f"background-color: {COLORS.surface};")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(SPACING.sm)

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {COLORS.surface};")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        self.source_row = QWidget(scroll_content)
        self.source_row.setStyleSheet(f"background-color: {COLORS.surface};")
        source_layout = QHBoxLayout(self.source_row)
        source_layout.setContentsMargins(0, 0, 0, 0)
        source_layout.setSpacing(SPACING.sm)
        self.source_label = QLabel(self.source_row)
        self.source_label.setObjectName("PopupSource")
        self.source_label.setWordWrap(True)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.source_label.setVisible(False)
        source_layout.addWidget(self.source_label, 1, Qt.AlignmentFlag.AlignTop)
        self.source_audio_button = LFButton(
            "",
            variant="ghost",
            icon_path=get_icon("audio"),
            icon_size=(16, 16),
        )
        self.source_audio_button.setFixedSize(28, 28)
        self.source_audio_button.setEnabled(False)
        source_layout.addWidget(
            self.source_audio_button,
            0,
            Qt.AlignmentFlag.AlignTop,
        )
        self.source_row.setVisible(False)
        scroll_layout.addWidget(self.source_row)

        divider_container = QWidget(scroll_content)
        divider_container.setStyleSheet(f"background-color: {COLORS.background};")
        divider_layout = QVBoxLayout(divider_container)
        divider_layout.setContentsMargins(0, SPACING.sm, 0, SPACING.sm)
        self.content_divider = QFrame(divider_container)
        self.content_divider.setFrameShape(QFrame.Shape.HLine)
        self.content_divider.setFrameShadow(QFrame.Shadow.Plain)
        self.content_divider.setFixedHeight(1)
        self.content_divider.setStyleSheet(f"background-color: {COLORS.border}; border: none;")
        divider_layout.addWidget(self.content_divider)
        scroll_layout.addWidget(divider_container)

        self.result_row = QWidget(scroll_content)
        self.result_row.setStyleSheet(f"background-color: {COLORS.surface};")
        result_layout = QHBoxLayout(self.result_row)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(SPACING.sm)
        self.result_label = QLabel(self.result_row)
        self.result_label.setObjectName("PopupResult")
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        result_layout.addWidget(self.result_label, 1, Qt.AlignmentFlag.AlignTop)
        self.result_audio_button = LFButton(
            "",
            variant="ghost",
            icon_path=get_icon("audio"),
            icon_size=(16, 16),
        )
        self.result_audio_button.setFixedSize(28, 28)
        self.result_audio_button.setEnabled(False)
        result_layout.addWidget(
            self.result_audio_button,
            0,
            Qt.AlignmentFlag.AlignTop,
        )
        scroll_layout.addWidget(self.result_row)

        self.scroll_area = QScrollArea(content)
        self.source_scroll_area = self.scroll_area
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setStyleSheet(
            f"QScrollArea {{ background-color: {COLORS.surface}; border: none; }}"
        )
        self.scroll_area.viewport().setStyleSheet(f"background-color: {COLORS.surface};")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setMaximumHeight(self.MAX_SCROLL_H)
        self.scroll_area.setWidget(scroll_content)
        layout.addWidget(self.scroll_area)

        self.label = self.result_label
        return content

    def _build_actions(self) -> QWidget:
        actions = QWidget(self)
        actions.setStyleSheet(f"""
            QWidget{{
                background-color: {COLORS.surface};
                border-bottom-left-radius: {RADIUS.card}px;
                border-bottom-right-radius: {RADIUS.card}px;
            }}
        """)
        layout = QHBoxLayout(actions)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        self.copy_button = LFButton(
            "Copy", variant="secondary", icon_path=get_icon("copy"), icon_size=(16, 16)
        )
        self.copy_button.clicked.connect(self._copy_result)
        self.retry_button = LFButton(
            "Retry", variant="secondary", icon_path=get_icon("refresh"), icon_size=(16, 16)
        )
        self.retry_button.clicked.connect(self.retry_requested.emit)
        self.sound_button = LFButton(
            "Sound", variant="secondary", icon_path=get_icon("audio"), icon_size=(16, 16)
        )
        self.sound_button.setEnabled(False)
        layout.addWidget(self.sound_button)
        self.dismiss_button = LFButton(
            "", variant="ghost", icon_path=get_icon("close"), icon_size=(16, 16)
        )
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
