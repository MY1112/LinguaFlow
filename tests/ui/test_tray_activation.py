"""系统托盘激活行为测试。"""

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from ui.tray import Tray


def test_tray_double_click_emits_open_request() -> None:
    QApplication.instance() or QApplication([])
    tray = Tray()
    opened: list[bool] = []
    tray.show_requested.connect(lambda: opened.append(True))

    tray._handle_activation(QSystemTrayIcon.ActivationReason.DoubleClick)

    assert opened == [True]
