"""LinguaFlow language selector component."""

from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtWidgets import QComboBox, QWidget

from ui.theme.theme import COLORS, RADIUS


class LFSelect(QComboBox):
    """Provide the shared selector dimensions and visual style."""

    def __init__(
        self,
        items: Iterable[str] = (),
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.addItems(list(items))
        self.setFixedSize(150, 36)
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS.surface};
                color: {COLORS.text};
                border: 1px solid {COLORS.border};
                border-radius: {RADIUS.large}px;
                padding: 0 12px;
                font-size: 14px;
            }}
            QComboBox:hover, QComboBox:focus {{
                border-color: {COLORS.primary};
            }}
            /* ===== 关键修复：下拉按钮区域 ===== */
            QComboBox::drop-down {{
                border: none;                 /* 清除所有默认边框（重点！消除竖分隔线） */
                background: transparent;
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: 32px;                 /* 给箭头预留宽度 */
            }}
            /* ===== 箭头图标 ===== */
            QComboBox::down-arrow {{
                /* 如果你有svg图标可以替换image，不用图标就保留原生箭头 */
                width: 14px;
                height: 14px;
            }}
            /* 下拉弹出面板样式（顺便补上，避免默认丑样式） */
            QComboBox QAbstractItemView {{
                background-color: {COLORS.surface};
                color: {COLORS.text};
                border: 1px solid {COLORS.border};
                border-radius: {RADIUS.medium}px;
                selection-background-color: {COLORS.primary};
                outline: none;
            }}
        """)
