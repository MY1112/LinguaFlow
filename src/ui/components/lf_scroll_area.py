from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget


class LimitScrollArea(QScrollArea):
    def __init__(self, max_height: int, parent=None):
        super().__init__(parent)
        self.max_h = max_height
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.inner_container = QWidget()
        self.inner_layout = QVBoxLayout(self.inner_container)
        self.setWidget(self.inner_container)

        # 布局变化自动重新计算高度
        self.inner_layout.sizeChanged.connect(self._auto_adjust_height)

    def _auto_adjust_height(self):
        content_height = self.inner_container.sizeHint().height()
        final_height = min(content_height, self.max_h)
        self.setFixedHeight(final_height)

    # 获取内部布局，添加卡片/组件
    def content_layout(self) -> QVBoxLayout:
        return self.inner_layout
