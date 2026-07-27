"""模型生命周期和推理服务。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from core.exceptions import LlamaCppAdapterError, ModelServiceError
from core.logger import get_logger
from integrations.llama_cpp import LlamaCppAdapter


class ModelService:
    """提供应用唯一的业务层模型接口。"""

    def __init__(
        self,
        logger: logging.Logger | None = None,
        adapter: LlamaCppAdapter | None = None,
    ) -> None:
        self._logger = logger or get_logger(__name__)
        self._adapter = adapter or LlamaCppAdapter(self._logger)

    def load_model(self, model_path: str) -> bool:
        """通过 llama.cpp 适配器加载模型。"""
        self._logger.info("正在加载模型：%s", model_path)
        try:
            loaded = self._adapter.load_model(Path(model_path))
        except LlamaCppAdapterError as error:
            self._logger.error("模型加载失败：%s", error)
            raise ModelServiceError(f"Model load failed: {model_path}") from error
        self._logger.info("模型加载完成：%s", model_path)
        return loaded

    def unload_model(self) -> None:
        """通过适配器卸载当前模型。"""
        self._logger.info("正在卸载模型")
        try:
            self._adapter.unload_model()
        except LlamaCppAdapterError as error:
            self._logger.error("模型卸载失败：%s", error)
            raise ModelServiceError("Model unload failed") from error
        self._logger.info("模型卸载完成")

    def is_loaded(self) -> bool:
        """返回适配器当前是否已加载模型。"""
        return self._adapter.is_loaded()

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_tokens: int = 128,
    ) -> str:
        """使用默认推理参数生成文本。"""
        self._logger.info("推理开始")
        try:
            raw_output = self._adapter.generate(
                prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            output = self._extract_text(raw_output)
        except LlamaCppAdapterError as error:
            self._logger.error("推理失败：%s", error)
            raise ModelServiceError("Inference failed") from error
        except (KeyError, IndexError, TypeError, ValueError) as error:
            self._logger.error("模型输出无效：%s", error)
            raise ModelServiceError("Invalid model output") from error
        self._logger.info("推理结束")
        return output

    def _extract_text(self, raw_output: Any) -> str:
        if not isinstance(raw_output, dict):
            raise TypeError("Model output is not a dictionary")
        choices = raw_output["choices"]
        if not isinstance(choices, list) or not choices:
            raise ValueError("Model output has no choices")
        text = choices[0]["text"]
        if not isinstance(text, str):
            raise TypeError("Model output text is not a string")
        return text
