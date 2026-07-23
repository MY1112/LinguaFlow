"""Main application window."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Empty shell window that delegates close handling to Application."""

    close_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("LinguaFlow")
        self.resize(960, 640)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Notify Application and keep the process alive in the tray."""
        event.ignore()
        self.close_requested.emit()
