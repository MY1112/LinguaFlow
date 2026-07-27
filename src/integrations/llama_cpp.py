"""唯一的 llama.cpp SDK 适配器。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from core.exceptions import LlamaCppAdapterError
from core.logger import get_logger


class LlamaCppAdapter:
    """封装所有与 llama.cpp Python SDK 的直接交互。"""

    _DEFAULT_STOP_SEQUENCES = ("<|im_end|>",)

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or get_logger(__name__)
        self._model: Any | None = None

    def load_model(self, model_path: str | Path, **kwargs: Any) -> bool:
        """加载 GGUF 模型，并先释放之前已加载的模型。"""
        path = Path(model_path)
        if not path.is_file():
            error = LlamaCppAdapterError(f"Model file does not exist: {path}")
            self._logger.error("无法加载模型：%s", error)
            raise error

        self.unload_model()
        try:
            from llama_cpp import Llama

            self._model = Llama(model_path=str(path), **kwargs)
        except Exception as error:
            self._logger.error("无法加载 llama.cpp 模型 %s：%s", path, error)
            self._model = None
            raise LlamaCppAdapterError(f"Unable to load model: {path}") from error
        return True

    def unload_model(self) -> None:
        """安全释放当前模型引用。"""
        self._model = None

    def is_loaded(self) -> bool:
        """返回当前是否已加载模型。"""
        return self._model is not None

    def generate(self, prompt: str, **kwargs: Any) -> Any:
        """调用并返回 llama.cpp 的原始响应。"""
        if self._model is None:
            error = LlamaCppAdapterError("No model is loaded")
            self._logger.error("无法生成输出：%s", error)
            raise error
        kwargs.setdefault("stop", list(self._DEFAULT_STOP_SEQUENCES))
        try:
            return self._model(prompt, **kwargs)
        except Exception as error:
            self._logger.error("无法生成输出：%s", error)
            raise LlamaCppAdapterError("Unable to generate output") from error
