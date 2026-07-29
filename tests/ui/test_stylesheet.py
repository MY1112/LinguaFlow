"""全局 Qt stylesheet 入口测试。"""

from ui.styles.stylesheet import build_stylesheet


def test_build_stylesheet_returns_global_qt_stylesheet() -> None:
    """stylesheet 入口应返回包含核心设计变量的 Qt 样式表。"""
    stylesheet = build_stylesheet()

    assert isinstance(stylesheet, str)
    assert "QWidget" in stylesheet
    assert "#F7F8FA" in stylesheet
    assert "#1A1D23" in stylesheet
    assert "QScrollBar:vertical" in stylesheet
    assert "QScrollBar::handle:vertical" in stylesheet
    assert "QScrollBar::handle:horizontal" in stylesheet
    assert "width: 10px" in stylesheet
    assert "height: 10px" in stylesheet
