"""AI Runtime 生命周期管理。"""

from __future__ import annotations

import logging
from pathlib import Path

from core.logger import get_logger
from runtime.runtime_state import RuntimeState
from services.config_service import ConfigService
from services.model_service import ModelService


class RuntimeManager:
    """初始化并释放与模型无关的 AI Runtime。"""

    def __init__(
        self,
        logger: logging.Logger | None = None,
        model_service: ModelService | None = None,
        config_service: ConfigService | None = None,
    ) -> None:
        self._logger = logger or get_logger(__name__)
        self._model_service = model_service or ModelService(self._logger)
        self._config_service = config_service
        self._state = RuntimeState()

    def initialize(self) -> None:
        """初始化 AI Runtime 框架，但不加载模型。"""
        if self._state.initialized:
            return
        self._state.initialized = True
        self._logger.info("AI Runtime 已初始化")
        self._load_configured_model()

    def shutdown(self) -> None:
        """释放模型资源并关闭 AI Runtime 框架。"""
        self._model_service.unload_model()
        if not self._state.initialized:
            return
        self._state = RuntimeState()
        self._logger.info("AI Runtime 已释放")

    def get_state(self) -> RuntimeState:
        """返回当前 Runtime 状态。"""
        return self._state

    def _load_configured_model(self) -> None:
        if self._config_service is None:
            self._logger.error(
                "\u65e0\u6cd5\u52a0\u8f7d\u6a21\u578b\uff1a\u672a\u63d0\u4f9b\u914d\u7f6e\u670d\u52a1"
            )
            return

        model_path_value = self._config_service.get("app.model_path")
        if not isinstance(model_path_value, str) or not model_path_value.strip():
            self._logger.error(
                "\u65e0\u6cd5\u52a0\u8f7d\u6a21\u578b\uff1a\u672a\u914d\u7f6e app.model_path"
            )
            return

        model_path = Path(model_path_value)
        if not model_path.is_absolute():
            model_path = self._config_service.config_directory.parent / model_path
        if not model_path.is_file():
            self._logger.error(
                "\u65e0\u6cd5\u52a0\u8f7d\u6a21\u578b\uff1a\u6587\u4ef6\u4e0d\u5b58\u5728 %s",
                model_path,
            )
            return

        try:
            self._model_service.load_model(str(model_path))
        except Exception as error:
            self._logger.error("\u6a21\u578b\u52a0\u8f7d\u5931\u8d25\uff1a%s", error)
            return

        self._state.model_loaded = True
        self._state.current_model_path = model_path
        self._logger.info("\u5df2\u52a0\u8f7d\u6a21\u578b\uff1a%s", model_path)
