"""应用主窗口。"""

from __future__ import annotations

import logging

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from core.logger import get_logger
from features.translation.translation_feature import TranslationFeature
from ui.workers.translation_worker import TranslationWorker


class MainWindow(QMainWindow):
    """提供翻译方向选择、原文输入和译文展示。"""

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
        self.resize(960, 640)
        self._build_ui()

    def closeEvent(self, event: QCloseEvent) -> None:
        """通知 Application，并保持进程在系统托盘中运行。"""
        event.ignore()
        self.close_requested.emit()

    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        direction_layout = QHBoxLayout()
        direction_layout.addWidget(QLabel("翻译方向"))
        self.direction_group = QButtonGroup(self)
        self.chinese_to_english_radio = QRadioButton("中文 → English")
        self.english_to_chinese_radio = QRadioButton("English → 中文")
        self.chinese_to_english_radio.setChecked(True)
        self.direction_group.addButton(self.chinese_to_english_radio)
        self.direction_group.addButton(self.english_to_chinese_radio)
        direction_layout.addWidget(self.chinese_to_english_radio)
        direction_layout.addWidget(self.english_to_chinese_radio)
        direction_layout.addStretch()
        layout.addLayout(direction_layout)

        layout.addWidget(QLabel("原文"))
        self.source_text_edit = QPlainTextEdit()
        self.source_text_edit.setPlaceholderText("请输入要翻译的文本")
        layout.addWidget(self.source_text_edit)

        self.translate_button = QPushButton("翻译")
        self.translate_button.clicked.connect(self._translate)
        layout.addWidget(self.translate_button)

        layout.addWidget(QLabel("译文"))
        self.target_text_edit = QPlainTextEdit()
        self.target_text_edit.setReadOnly(True)
        layout.addWidget(self.target_text_edit)

        self.setCentralWidget(central_widget)

    def _translate(self) -> None:
        text = self.source_text_edit.toPlainText()
        source_language, target_language = self._get_translation_direction()
        self._logger.info(
            "点击翻译，源语言：%s，目标语言：%s",
            source_language,
            target_language,
        )
        self.translate_button.setEnabled(False)
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
        self._logger.info("翻译完成")

    def _on_translation_failed(self, message: str) -> None:
        self.translate_button.setEnabled(True)
        self._logger.error("翻译异常：%s", message)
        QMessageBox.warning(self, "翻译失败", message)

    def _clear_translation_thread(self) -> None:
        self._translation_thread = None
        self._translation_worker = None

    def _get_translation_direction(self) -> tuple[str, str]:
        if self.english_to_chinese_radio.isChecked():
            return "英文", "中文"
        return "中文", "英文"
