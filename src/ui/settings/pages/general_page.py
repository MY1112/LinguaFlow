"""Settings General page."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel

from services.config_service import ConfigService
from ui.components.lf_card import LFCard
from ui.theme.theme import COLORS


class GeneralPage(LFCard):
    """展示应用级设置的页面骨架。"""

    def __init__(self, config_service: ConfigService | None = None) -> None:
        super().__init__(padding=24)
        self.title_label = QLabel("General", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        app_name = config_service.get("app.name", "LinguaFlow") if config_service else "LinguaFlow"
        self.app_name_label = QLabel(str(app_name), self)
        self.theme_label = QLabel("Theme", self)
        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(["System", "Light", "Dark"])
        self.launch_at_startup_check = QCheckBox("Launch at startup", self)
        self.close_to_tray_check = QCheckBox("Close to tray", self)
        self.popup_duration_label = QLabel("Popup display time: 2000 ms", self)
        self.description_label = QLabel("Application preferences", self)
        self.description_label.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.app_name_label)
        self.layout().addWidget(self.theme_label)
        self.layout().addWidget(self.theme_combo)
        self.layout().addWidget(self.launch_at_startup_check)
        self.layout().addWidget(self.close_to_tray_check)
        self.layout().addWidget(self.popup_duration_label)
        self.layout().addWidget(self.description_label)
        self.layout().addStretch()
