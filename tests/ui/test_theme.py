"""UI Theme 基础设施测试。"""

from ui.theme.theme import COLORS, RADIUS, SPACING, Theme


def test_theme_exposes_required_design_tokens() -> None:
    """Theme 应集中暴露颜色、圆角和间距设计变量。"""
    assert COLORS.background == "#F7F8FA"
    assert COLORS.surface == "#FFFFFF"
    assert COLORS.primary == "#5B8DEF"
    assert COLORS.text == "#1A1D23"
    assert COLORS.secondary_text == "#6B7280"
    assert COLORS.border == "#E9EDF3"
    assert COLORS.success == "#84C97C"
    assert COLORS.error == "#FF6B6B"

    assert RADIUS.small == 4
    assert RADIUS.medium == 8
    assert RADIUS.large == 12

    assert SPACING.xs == 4
    assert SPACING.sm == 8
    assert SPACING.md == 16
    assert SPACING.lg == 24
    assert SPACING.xl == 32

    assert Theme.colors == COLORS
    assert Theme.radius == RADIUS
    assert Theme.spacing == SPACING
