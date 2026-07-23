"""Application lifecycle coordinator."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.logger import configure_logging
from runtime.app_context import AppContext
from services.config_service import ConfigService
from ui.main_window import MainWindow
from ui.tray import Tray


class Application:
    """Own and coordinate the desktop application's runtime objects."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        logger = configure_logging(project_root / "logs")
        config_service = ConfigService(project_root / "config")
        self.application = QApplication(sys.argv)
        self.application.setQuitOnLastWindowClosed(False)
        self.context = AppContext(logger=logger, config_service=config_service)
        self.main_window = MainWindow()
        self.tray = Tray()
        self._connect_signals()

    def run(self) -> int:
        """Initialize the desktop shell and start the Qt event loop."""
        self.main_window.show()
        self.tray.show()
        self.context.logger.info("LinguaFlow started")
        exit_code = self.application.exec()
        self.context.logger.info("LinguaFlow stopped")
        return exit_code

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
        self.tray.hide()
        self.application.quit()
