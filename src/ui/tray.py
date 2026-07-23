"""System tray integration for the desktop application."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QApplication, QStyle, QSystemTrayIcon


class Tray(QObject):
    """System tray icon and menu without knowledge of the main window."""

    show_requested = Signal()
    quit_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self._create_icon())
        self.tray_icon.setToolTip("LinguaFlow")
        self.tray_icon.setContextMenu(self._create_menu())
        self.tray_icon.activated.connect(self._handle_activation)

    def show(self) -> None:
        """Show the system tray icon."""
        self.tray_icon.show()

    def hide(self) -> None:
        """Hide the system tray icon."""
        self.tray_icon.hide()

    def _create_icon(self) -> QIcon:
        style = QApplication.style()
        return style.standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)

    def _create_menu(self) -> QMenu:
        menu = QMenu()
        open_action = QAction("打开 LinguaFlow", menu)
        quit_action = QAction("退出", menu)
        open_action.triggered.connect(self.show_requested.emit)
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(open_action)
        menu.addAction(quit_action)
        return menu

    def _handle_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_requested.emit()
