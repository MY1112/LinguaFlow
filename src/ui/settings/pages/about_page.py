"""Settings About page."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel

from services.config_service import ConfigService
from ui.components.lf_card import LFCard
from ui.theme.theme import COLORS


class AboutPage(LFCard):
    """展示 LinguaFlow 版本与技术栈信息。"""

    def __init__(self, config_service: ConfigService | None = None) -> None:
        super().__init__(padding=24)
        self.title_label = QLabel("About", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        app_name = config_service.get("app.name", "LinguaFlow") if config_service else "LinguaFlow"
        version = config_service.get("app.version", "v1.0") if config_service else "v1.0"
        self.name_label = QLabel(str(app_name), self)
        self.version_label = QLabel(str(version), self)
        self.tech_stack_label = QLabel("Python · PySide6 · llama.cpp", self)
        self.description_label = QLabel("Local-first desktop AI assistant", self)
        for label in (self.tech_stack_label, self.description_label):
            label.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.name_label)
        self.layout().addWidget(self.version_label)
        self.layout().addWidget(self.tech_stack_label)
        self.layout().addWidget(self.description_label)
        self.layout().addStretch()
