"""Main application window."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from runtime.app_context import AppContext


class MainWindow(QMainWindow):
    """Empty shell window for the Bootstrap version."""

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.setWindowTitle(str(context.config_service.get("app.name", "LinguaFlow")))
        self.resize(960, 640)
