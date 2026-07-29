from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QSizePolicy


# 自定义可点击图标Label
class LFIconLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        # 关键！和LFButton保持一致，禁止布局挤压
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)
