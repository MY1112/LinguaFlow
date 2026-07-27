"""应用生命周期协调器。"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QObject, QThread, QTimer
from PySide6.QtWidgets import QApplication

from core.logger import configure_logging
from features.translation.translation_feature import TranslationFeature
from integrations.hotkey import HotkeyAdapter
from integrations.selection import SelectionAdapter
from runtime.app_context import AppContext
from runtime.runtime_manager import RuntimeManager
from services.config_service import ConfigService
from services.model_service import ModelService
from services.prompt_service import PromptService
from ui.main_window import MainWindow
from ui.popup_window import PopupWindow
from ui.tray import Tray
from ui.workers.translation_worker import TranslationWorker


class Application(QObject):
    """统一管理桌面应用的生命周期对象。"""

    def __init__(self) -> None:
        super().__init__()
        project_root = Path(__file__).resolve().parents[2]
        logger = configure_logging(project_root / "logs")
        config_service = ConfigService(project_root / "config")
        model_service = ModelService(logger)
        prompt_service = PromptService(logger)
        translation_feature = TranslationFeature(prompt_service, model_service, logger)
        runtime = RuntimeManager(
            logger=logger,
            model_service=model_service,
            config_service=config_service,
        )
        self.application = QApplication(sys.argv)
        self.application.setQuitOnLastWindowClosed(False)
        self.context = AppContext(
            logger=logger,
            config_service=config_service,
            runtime=runtime,
            prompt_service=prompt_service,
        )
        self.translation_feature = translation_feature
        self.main_window = MainWindow(translation_feature, logger)
        self.popup_window = PopupWindow(logger)
        self.tray = Tray()
        self.hotkey_adapter = HotkeyAdapter(
            self._schedule_selection_translation,
            logger,
            window_handle=int(self.main_window.winId()),
        )
        self.selection_adapter = SelectionAdapter(logger)
        self._selection_translation_thread: QThread | None = None
        self._selection_translation_worker: TranslationWorker | None = None
        self._connect_signals()

    def run(self) -> int:
        """初始化 Runtime 并启动 Qt 事件循环。"""
        self.context.runtime.initialize()
        self.hotkey_adapter.register()
        self.main_window.show()
        self.tray.show()
        self.context.logger.info("LinguaFlow 启动")
        try:
            return self.application.exec()
        finally:
            self.hotkey_adapter.unregister()
            self.tray.hide()
            self.context.runtime.shutdown()
            self.context.logger.info("LinguaFlow 停止")

    def _connect_signals(self) -> None:
        self.selection_adapter.capture_finished.connect(self._on_selection_captured)
        self.main_window.close_requested.connect(self._hide_to_tray)
        self.tray.show_requested.connect(self._show_window)
        self.tray.quit_requested.connect(self._quit)

    def _hide_to_tray(self) -> None:
        self.main_window.hide()

    def _show_window(self) -> None:
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def _schedule_selection_translation(self) -> None:
        """将划词读取延后到快捷键原生事件处理完成后。"""
        foreground_hwnd = getattr(
            getattr(self, "hotkey_adapter", None), "last_foreground_window", 0
        )
        if foreground_hwnd:
            QTimer.singleShot(0, lambda: self._translate_selection(foreground_hwnd))
        else:
            QTimer.singleShot(0, self._translate_selection)

    def _translate_selection(self, foreground_hwnd: int | None = None) -> None:
        """异步请求 SelectionAdapter 捕获选中文本。"""
        self.context.logger.info("开始划词翻译流程")
        if not self.selection_adapter.capture_selected_text(foreground_hwnd):
            self.context.logger.info("选中文本捕获任务正在执行")

    def _on_selection_captured(self, selected_text: str) -> None:
        """接收 SelectionAdapter 的捕获结果并继续翻译流程。"""
        if not selected_text.strip():
            self.context.logger.info("未获取到选中文本，结束划词翻译流程")
            return
        self._start_selection_translation(selected_text)

    def _start_selection_translation(self, text: str) -> None:
        """创建后台 Worker 执行划词翻译。"""
        if self._selection_translation_thread is not None:
            self.context.logger.warning("已有划词翻译任务正在执行")
            return

        thread = QThread(self.application)
        worker = TranslationWorker(
            self.translation_feature,
            text,
            "中文",
            "英文",
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._on_selection_translation_finished)
        worker.failed.connect(self._on_selection_translation_failed)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._clear_selection_translation)
        self._selection_translation_thread = thread
        self._selection_translation_worker = worker
        self.context.logger.info("启动划词翻译后台任务")
        thread.start()

    def _on_selection_translation_finished(self, result: str) -> None:
        """接收 Worker 的成功结果并显示 Popup。"""
        self.context.logger.info("划词翻译完成")
        self.popup_window.show_result(result)

    def _on_selection_translation_failed(self, message: str) -> None:
        """记录详细错误，并显示统一的失败提示。"""
        self.context.logger.error("划词翻译失败：%s", message)
        self.popup_window.show_result("翻译失败")

    def _clear_selection_translation(self) -> None:
        """清理已完成的划词翻译 Worker 引用。"""
        self._selection_translation_thread = None
        self._selection_translation_worker = None

    def _quit(self) -> None:
        self.application.quit()
