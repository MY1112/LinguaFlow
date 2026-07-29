"""MainWindow implementation for the M4-004 visual layout."""

from __future__ import annotations

import logging

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QCloseEvent, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.logger import get_logger
from features.translation.translation_feature import TranslationFeature
from ui.components.lf_button import LFButton
from ui.components.lf_card import LFCard
from ui.components.lf_header import LFHeader
from ui.components.lf_input import LFInput
from ui.components.lf_select import LFSelect
from ui.components.lf_status import LFStatus
from ui.resources.assets import get_favicon, get_icon
from ui.theme.theme import COLORS, SPACING
from ui.workers.translation_worker import TranslationWorker


class MainWindow(QMainWindow):
    """Main translation workspace."""

    close_requested = Signal()

    def __init__(
        self,
        translation_feature: TranslationFeature,
        logger: logging.Logger | None = None,
    ) -> None:
        super().__init__()
        self._logger = logger or get_logger(__name__)
        self._translation_feature = translation_feature
        self._translation_thread: QThread | None = None
        self._translation_worker: TranslationWorker | None = None
        self.setWindowTitle("LinguaFlow")
        self.setWindowIcon(QIcon(str(get_favicon())))
        self.resize(420, 620)
        self.setMinimumSize(420, 520)
        self._build_ui()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Ask Application to hide the window in the system tray."""
        event.ignore()
        self.close_requested.emit()

    def _build_ui(self) -> None:
        central = QWidget(self)
        central.setStyleSheet(f"background-color: {COLORS.background};")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(SPACING.lg, SPACING.xl - SPACING.xs, SPACING.lg, 0)
        layout.setSpacing(SPACING.md)

        self.header = LFHeader(central)
        self.logo_label = self.header.logo_label
        layout.addWidget(self.header)
        layout.addWidget(self._build_language_selector(central))
        layout.addWidget(self._build_input_card(central))
        layout.addWidget(self._build_translate_button(central))
        layout.addWidget(self._build_result_card(central))
        self.status_bar = self._build_status_bar(central)
        layout.addWidget(self.status_bar)
        self.setCentralWidget(central)

        self._translate_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self._translate_shortcut.activated.connect(self._translate)

    def _build_language_selector(self, parent: QWidget) -> QWidget:
        area = QWidget(parent)
        layout = QHBoxLayout(area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING.sm)
        self.source_language = LFSelect(["中文", "English"], area)
        self.target_language = LFSelect(["中文", "English"], area)
        self.target_language.setCurrentIndex(1)
        self.swap_button = LFButton(
            "", variant="ghost", icon_path=get_icon("swap"), icon_size=(16, 16)
        )
        self.swap_button.setFixedSize(40, 36)
        self.swap_button.clicked.connect(self._swap_languages)
        layout.addWidget(self.source_language)
        layout.addWidget(self.swap_button)
        layout.addWidget(self.target_language)
        layout.addStretch()
        return area

    def _build_input_card(self, parent: QWidget) -> LFCard:
        self.input_card = LFCard(parent, padding=0)
        self.input_card.setFixedSize(372, 160)
        card_layout = self.input_card.layout()
        if card_layout is None:
            raise RuntimeError("Input card layout is missing")

        self.source_text_edit = LFInput(max_length=5000)
        self.source_text_edit.setPlaceholderText("Enter text to translate...")
        self.source_text_edit.setFixedHeight(160)
        self.source_text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card_layout.addWidget(self.source_text_edit)

        return self.input_card

    def _build_translate_button(self, parent: QWidget) -> QWidget:
        area = QWidget(parent)
        layout = QHBoxLayout(area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        self.translate_button = LFButton(
            "Translate", variant="primary", icon_path=get_icon("star"), icon_size=(16, 16)
        )
        self.translate_button.setFixedSize(240, 44)
        self.translate_button.clicked.connect(self._translate)
        layout.addWidget(self.translate_button)
        layout.addStretch()
        return area

    def _build_result_card(self, parent: QWidget) -> LFCard:
        self.result_card = LFCard(parent)
        self.result_card.setFixedSize(372, 160)
        card_layout = self.result_card.layout()
        if card_layout is None:
            raise RuntimeError("Result card layout is missing")
        heading = QHBoxLayout()
        self.result_title = QLabel("Translation Result", self.result_card)
        self.result_title.setStyleSheet(f"color: {COLORS.text}; font-size: 15px; font-weight: 600;")
        heading.addWidget(self.result_title)
        heading.addStretch()
        card_layout.addLayout(heading)
        self.target_text_edit = QPlainTextEdit(self.result_card)
        self.target_text_edit.setReadOnly(True)
        self.target_text_edit.setPlaceholderText("Your translation will appear here...")
        self.target_text_edit.setFixedHeight(64)
        self.target_text_edit.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS.surface};
                color: {COLORS.text};
                border: 0;
                font-size: 14px;
            }}
            """)
        card_layout.addWidget(self.target_text_edit)
        actions = QHBoxLayout()
        actions.addStretch()
        self.copy_button = LFButton(
            "", variant="ghost", icon_path=get_icon("copy"), icon_size=(16, 16)
        )
        self.copy_button.setFixedSize(32, 32)
        self.copy_button.clicked.connect(self._copy_result)
        self.sound_button = LFButton(
            "", variant="ghost", icon_path=get_icon("audio"), icon_size=(16, 16)
        )
        self.sound_button.setFixedSize(32, 32)
        self.sound_button.setEnabled(False)
        actions.addWidget(self.copy_button)
        actions.addWidget(self.sound_button)
        card_layout.addLayout(actions)
        return self.result_card

    def _build_status_bar(self, parent: QWidget) -> QWidget:
        status_bar = QWidget(parent)
        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(0, 0, 0, 0)
        self.model_status = LFStatus("Model Ready", variant="success")
        layout.addWidget(self.model_status)
        layout.addStretch()
        layout.addWidget(QLabel("Qwen2.5-3B", status_bar))
        layout.addStretch()
        layout.addWidget(QLabel("Alt + Q", status_bar))
        layout.addStretch()
        self.setting_button = LFButton(
            "", variant="ghost", icon_path=get_icon("setting"), icon_size=(16, 16)
        )
        self.setting_button.setFixedSize(16, 16)
        layout.addWidget(self.setting_button)
        return status_bar

    def _swap_languages(self) -> None:
        source_index = self.source_language.currentIndex()
        target_index = self.target_language.currentIndex()
        self.source_language.setCurrentIndex(target_index)
        self.target_language.setCurrentIndex(source_index)

    def _copy_result(self) -> None:
        from PySide6.QtWidgets import QApplication

        QApplication.clipboard().setText(self.target_text_edit.toPlainText())

    def _translate(self) -> None:
        text = self.source_text_edit.toPlainText()
        source_language, target_language = self._get_translation_direction()
        self._logger.info(
            "Translate clicked, source=%s, target=%s",
            source_language,
            target_language,
        )
        self.translate_button.setEnabled(False)
        self.translate_button.setText("Translating...")
        self.model_status.set_status("Translating...", "loading")
        thread = QThread(self)
        worker = TranslationWorker(
            self._translation_feature,
            text,
            source_language,
            target_language,
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._on_translation_finished)
        worker.failed.connect(self._on_translation_failed)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._clear_translation_thread)
        self._translation_thread = thread
        self._translation_worker = worker
        thread.start()

    def _on_translation_finished(self, result: str) -> None:
        self.target_text_edit.setPlainText(result)
        self.translate_button.setEnabled(True)
        self.translate_button.setText("Translate")
        self.model_status.set_status("Model Ready", "success")
        self._logger.info("Translation completed")

    def _on_translation_failed(self, message: str) -> None:
        self.translate_button.setEnabled(True)
        self.translate_button.setText("Translate")
        self.model_status.set_status("Model Error", "error")
        self._logger.error("Translation failed: %s", message)
        QMessageBox.warning(self, "Translation Failed", message)

    def _clear_translation_thread(self) -> None:
        self._translation_thread = None
        self._translation_worker = None

    def _get_translation_direction(self) -> tuple[str, str]:
        return self.source_language.currentText(), self.target_language.currentText()
