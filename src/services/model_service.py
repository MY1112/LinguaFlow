"""Model lifecycle and inference service."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from core.exceptions import LlamaCppAdapterError, ModelServiceError
from core.logger import get_logger
from integrations.llama_cpp import LlamaCppAdapter


class ModelService:
    """Provide the application's single business-level model interface."""

    def __init__(
        self,
        logger: logging.Logger | None = None,
        adapter: LlamaCppAdapter | None = None,
    ) -> None:
        self._logger = logger or get_logger(__name__)
        self._adapter = adapter or LlamaCppAdapter(self._logger)

    def load_model(self, model_path: str) -> bool:
        """Load a model through the llama.cpp adapter."""
        self._logger.info("Loading model: %s", model_path)
        try:
            loaded = self._adapter.load_model(Path(model_path))
        except LlamaCppAdapterError as error:
            self._logger.error("Model load failed: %s", error)
            raise ModelServiceError(f"Model load failed: {model_path}") from error
        self._logger.info("Model loaded: %s", model_path)
        return loaded

    def unload_model(self) -> None:
        """Unload the current model through the adapter."""
        self._logger.info("Unloading model")
        try:
            self._adapter.unload_model()
        except LlamaCppAdapterError as error:
            self._logger.error("Model unload failed: %s", error)
            raise ModelServiceError("Model unload failed") from error
        self._logger.info("Model unloaded")

    def is_loaded(self) -> bool:
        """Return whether the adapter currently has a loaded model."""
        return self._adapter.is_loaded()

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_tokens: int = 512,
    ) -> str:
        """Generate text with default inference parameters."""
        self._logger.info("Inference started")
        try:
            raw_output = self._adapter.generate(
                prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            output = self._extract_text(raw_output)
        except LlamaCppAdapterError as error:
            self._logger.error("Inference failed: %s", error)
            raise ModelServiceError("Inference failed") from error
        except (KeyError, IndexError, TypeError, ValueError) as error:
            self._logger.error("Invalid model output: %s", error)
            raise ModelServiceError("Invalid model output") from error
        self._logger.info("Inference finished")
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
