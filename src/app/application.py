"""应用生命周期协调器。"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.logger import configure_logging
from runtime.app_context import AppContext
from runtime.runtime_manager import RuntimeManager
from services.config_service import ConfigService
from services.model_service import ModelService
from services.prompt_service import PromptService
from ui.main_window import MainWindow
from ui.tray import Tray


class Application:
    """统一管理桌面应用的生命周期对象。"""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        logger = configure_logging(project_root / "logs")
        config_service = ConfigService(project_root / "config")
        model_service = ModelService(logger)
        prompt_service = PromptService(logger)
        runtime = RuntimeManager(logger, model_service)
        self.application = QApplication(sys.argv)
        self.application.setQuitOnLastWindowClosed(False)
        self.context = AppContext(
            logger=logger,
            config_service=config_service,
            runtime=runtime,
            prompt_service=prompt_service,
        )
        self.main_window = MainWindow()
        self.tray = Tray()
        self._connect_signals()

    def run(self) -> int:
        """初始化 Runtime 并启动 Qt 事件循环。"""
        self.context.runtime.initialize()
        self.main_window.show()
        self.tray.show()
        self.context.logger.info("LinguaFlow 启动")
        try:
            return self.application.exec()
        finally:
            self.tray.hide()
            self.context.runtime.shutdown()
            self.context.logger.info("LinguaFlow 停止")

    def _connect_signals(self) -> None:
        self.main_window.close_requested.connect(self._hide_to_tray)
        self.tray.show_requested.connect(self._show_window)
        self.tray.quit_requested.connect(self._quit)

    def _hide_to_tray(self) -> None:
        self.main_window.hide()

    def _show_window(self) -> None:
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def _quit(self) -> None:
        self.application.quit()
