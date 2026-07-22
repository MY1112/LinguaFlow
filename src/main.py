"""LinguaFlow application entry point."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.logger import configure_logging
from runtime.app_context import AppContext
from services.config_service import ConfigService
from ui.main_window import MainWindow


def main() -> int:
    """Create the application, show the empty window, and run its event loop."""
    project_root = Path(__file__).resolve().parents[1]
    logger = configure_logging(project_root / "logs")
    config_service = ConfigService(project_root / "config")
    context = AppContext(logger=logger, config_service=config_service)

    application = QApplication(sys.argv)
    context.main_window = MainWindow(context)
    context.main_window.show()
    logger.info("LinguaFlow started")
    exit_code = application.exec()
    logger.info("LinguaFlow stopped")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
