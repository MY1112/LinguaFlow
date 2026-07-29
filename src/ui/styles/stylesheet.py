"""全局 Qt stylesheet 入口。"""

from __future__ import annotations

from ui.theme.theme import COLORS, RADIUS


def build_stylesheet() -> str:
    """构建应用级 Qt stylesheet。"""
    return f"""
QWidget {{
    background-color: {COLORS.background};
    color: {COLORS.text};
}}

QLineEdit, QPlainTextEdit, QTextEdit, QComboBox {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: {RADIUS.large}px;
}}

QScrollBar:vertical {{
    width: 10px;
    background: transparent;
    border: none;
}}

QScrollBar:horizontal {{
    height: 10px;
    background: transparent;
    border: none;
}}

QScrollBar::handle:vertical,
QScrollBar::handle:horizontal {{
    background: {COLORS.scrollbar_thumb};
    border: none;
    border-radius: 4px;
    min-height: 24px;
    min-width: 24px;
}}

QScrollBar::handle:vertical:hover,
QScrollBar::handle:horizontal:hover {{
    background: {COLORS.scrollbar_thumb_hover};
}}

QScrollBar::handle:vertical:pressed,
QScrollBar::handle:horizontal:pressed {{
    background: {COLORS.scrollbar_thumb_active};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0;
    height: 0;
    border: none;
    background: transparent;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: transparent;
}}
""".strip()
