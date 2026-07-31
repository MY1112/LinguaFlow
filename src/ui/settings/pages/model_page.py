"""Settings Model page."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QLabel

from services.config_service import ConfigService
from ui.components.lf_card import LFCard
from ui.theme.theme import COLORS


class ModelPage(LFCard):
    """展示当前本地模型信息的页面。"""

    def __init__(self, config_service: ConfigService | None = None) -> None:
        super().__init__(padding=24)
        self.title_label = QLabel("Model", self)
        self.title_label.setStyleSheet(f"color: {COLORS.text}; font-size: 20px; font-weight: 600;")
        model_path = config_service.get("app.model_path", "") if config_service else ""
        model_path = str(model_path or "")
        self.model_name_label = QLabel(
            Path(model_path).stem if model_path else "Not configured", self
        )
        self.model_path_label = QLabel(model_path or "Not configured", self)
        self.model_status_label = QLabel("Configured" if model_path else "Not configured", self)
        self.description_label = QLabel("Local model information", self)
        self.description_label.setStyleSheet(f"color: {COLORS.secondary_text}; font-size: 14px;")
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.model_name_label)
        self.layout().addWidget(self.model_path_label)
        self.layout().addWidget(self.model_status_label)
        self.layout().addWidget(self.description_label)
        self.layout().addStretch()
