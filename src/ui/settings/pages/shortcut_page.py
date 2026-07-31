"""Settings Shortcut page."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel

from services.config_service import ConfigService
from ui.components.lf_card import LFCard
from ui.theme.theme import COLORS


class ShortcutPage(LFCard):
    """展示当前全局快捷键并预留修改入口。"""

    def __init__(self, config_service: ConfigService | None = None) -> None:
        super().__init__(padding=24)
        self.title_label = QLabel("Shortcut", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        shortcut = "Alt + Q"
        if config_service:
            shortcut = str(
                config_service.hotkeys.get("translate_selection")
                or config_service.hotkeys.get("selection_translation")
                or shortcut
            )
        self.shortcut_label = QLabel(shortcut, self)
        self.edit_shortcut_label = QLabel("Change shortcut (coming later)", self)
        self.description_label = QLabel("Global shortcut preferences", self)
        for label in (self.edit_shortcut_label, self.description_label):
            label.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.shortcut_label)
        self.layout().addWidget(self.edit_shortcut_label)
        self.layout().addWidget(self.description_label)
        self.layout().addStretch()
