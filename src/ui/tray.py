"""桌面应用的系统托盘集成。"""

from __future__ import annotations

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QMenu, QSystemTrayIcon, QWidget, QWidgetAction

from ui.resources.assets import get_favicon, get_icon


class LFTrayMenu(QMenu):
    """LinguaFlow 系统托盘菜单。"""

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.open_action = self._add_action("LinguaFlow", "title_action", "logo_16")
        self._add_separator(color="#eff1f4", height=1)
        self.open_action = self._add_action("打开主窗口", "open_action", "chat")
        self.pause_action = self._add_action("暂停划词翻译", "pause_action", "pause")
        self.settings_action = self._add_action("设置", "settings_action", "settings")
        self._add_separator(color="#eff1f4", height=1)
        self.exit_action = self._add_action("退出", "exit_action", "exit")

    def _add_action(self, text: str, object_name: str, icon_name: str | None = None) -> QAction:
        action = QAction(text, self)
        action.setObjectName(object_name)
        if icon_name:
            pix_path = str(get_icon(icon_name))
            pix = QPixmap(pix_path)
            scaled_pix = pix.scaled(
                14,
                14,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            action.setIcon(QIcon(scaled_pix))
        self.addAction(action)
        return action

    def set_paused(self, paused: bool) -> None:
        """更新暂停菜单项的显示状态。"""
        self.pause_action.setText("恢复划词翻译" if paused else "暂停划词翻译")

    def _add_separator(self, color: str, height: int = 1):
        """自定义可设置颜色/粗细的分隔线（修复塌陷问题）"""
        # 外层容器，防止尺寸塌陷
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)  # 分隔线左右、上下外边距
        layout.setSpacing(0)

        line = QFrame()
        line.setFixedHeight(height)
        line.setStyleSheet(f"background-color: {color};")
        layout.addWidget(line)

        action = QWidgetAction(self)
        action.setDefaultWidget(container)
        self.addAction(action)


class Tray(QObject):
    """提供系统托盘图标、菜单和生命周期管理。"""

    show_requested = Signal()
    quit_requested = Signal()
    translate_selection_requested = Signal()
    pause_requested = Signal()
    settings_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self._create_icon())
        self.tray_icon.setToolTip("LinguaFlow")
        self.menu = self._create_menu()
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self._handle_activation)

    def show(self) -> None:
        """显示系统托盘图标。"""
        self.tray_icon.show()

    def hide(self) -> None:
        """隐藏系统托盘图标。"""
        self.tray_icon.hide()

    def set_paused(self, paused: bool) -> None:
        """同步应用暂停状态到托盘菜单。"""
        self.menu.set_paused(paused)

    def _create_icon(self) -> QIcon:
        return QIcon(str(get_favicon()))

    def _create_menu(self) -> LFTrayMenu:
        menu = LFTrayMenu()
        menu.open_action.triggered.connect(self.show_requested.emit)
        menu.pause_action.triggered.connect(self.pause_requested.emit)
        menu.settings_action.triggered.connect(self.settings_requested.emit)
        menu.exit_action.triggered.connect(self.quit_requested.emit)
        return menu

    def _handle_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_requested.emit()
