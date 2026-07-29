"""LinguaFlow UI 设计变量。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    """集中定义 UI 使用的颜色。"""

    background: str = "#F7F8FA"
    surface: str = "#FFFFFF"
    primary: str = "#5B8DEF"
    text: str = "#1A1D23"
    secondary_text: str = "#6B7280"
    border: str = "#E9EDF3"
    scrollbar_thumb: str = "#CAD5E5"
    scrollbar_thumb_hover: str = "#BAC7D9"
    scrollbar_thumb_active: str = "#ABBBD1"
    success: str = "#84C97C"
    error: str = "#FF6B6B"


@dataclass(frozen=True)
class Radius:
    """集中定义 UI 使用的圆角。"""

    small: int = 4
    medium: int = 8
    large: int = 12
    card: int = 16
    pill: int = 999


@dataclass(frozen=True)
class Spacing:
    """集中定义 UI 使用的间距。"""

    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32


COLORS = Colors()
RADIUS = Radius()
SPACING = Spacing()


class Theme:
    """UI 设计变量的统一入口。"""

    colors = COLORS
    radius = RADIUS
    spacing = SPACING
