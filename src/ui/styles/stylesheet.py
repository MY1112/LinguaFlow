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
""".strip()
