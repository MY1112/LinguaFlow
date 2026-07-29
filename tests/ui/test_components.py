"""公共 UI 组件测试。"""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication

from ui.components.lf_button import LFButton
from ui.components.lf_card import LFCard
from ui.components.lf_input import LFInput
from ui.components.lf_status import LFStatus


@pytest.fixture(scope="session")
def qt_application() -> QApplication:
    """提供 Qt 测试应用实例。"""
    return QApplication.instance() or QApplication([])


def test_lf_button_supports_primary_variant(qt_application: QApplication) -> None:
    """LFButton 应提供统一的 Primary 按钮组件。"""
    button = LFButton("Translate", variant="primary")

    assert button.text() == "Translate"
    assert button.variant == "primary"
    assert button.minimumHeight() == 42


def test_lf_card_uses_card_style(qt_application: QApplication) -> None:
    """LFCard 应提供统一的卡片容器。"""
    card = LFCard()

    assert card.objectName() == "LFCard"
    assert card.layout() is not None


def test_lf_input_limits_text_and_exposes_text_changed(qt_application: QApplication) -> None:
    """LFInput 应支持占位文本和最大长度限制。"""
    input_widget = LFInput(max_length=5)
    input_widget.setPlainText("123456")

    assert input_widget.toPlainText() == "12345"
    assert input_widget.maximum_length == 5


def test_lf_input_shows_internal_character_count_by_default(qt_application: QApplication) -> None:
    """LFInput should own and update its character counter by default."""
    input_widget = LFInput(max_length=5)

    assert not input_widget.count_label.isHidden()
    assert input_widget.count_label.text() == "0 / 5"

    input_widget.setPlainText("123")

    assert input_widget.count_label.text() == "3 / 5"


def test_lf_input_counter_reserves_space_for_text(qt_application: QApplication) -> None:
    """LFInput should size the counter so the full value remains visible."""
    input_widget = LFInput(max_length=5000)
    input_widget.resize(200, 80)
    input_widget.show()
    qt_application.processEvents()

    input_widget.setPlainText("123")
    qt_application.processEvents()

    assert input_widget.count_label.width() >= 40
    input_widget.close()


def test_lf_input_can_hide_internal_character_count(qt_application: QApplication) -> None:
    """LFInput should hide its internal counter when disabled."""
    input_widget = LFInput(max_length=5, show_count=False)

    assert not input_widget.count_label.isVisible()


def test_lf_status_displays_variant_and_text(qt_application: QApplication) -> None:
    """LFStatus 应显示统一的状态文案。"""
    status = LFStatus("Model Ready", variant="success")

    assert status.text == "Model Ready"
    assert status.variant == "success"
    assert status.label.text() == "Model Ready"
