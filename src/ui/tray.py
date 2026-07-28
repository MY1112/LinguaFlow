"""桌面应用的系统托盘集成。"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon
from ui.resources.assets import get_favicon


class Tray(QObject):
    """提供系统托盘图标和菜单，不感知主窗口实现。"""

    show_requested = Signal()
    quit_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self._create_icon())
        self.tray_icon.setToolTip("LinguaFlow")
        self.tray_icon.setContextMenu(self._create_menu())
        self.tray_icon.activated.connect(self._handle_activation)

    def show(self) -> None:
        """显示系统托盘图标。"""
        self.tray_icon.show()

    def hide(self) -> None:
        """隐藏系统托盘图标。"""
        self.tray_icon.hide()

    def _create_icon(self) -> QIcon:
        return QIcon(str(get_favicon()))

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
