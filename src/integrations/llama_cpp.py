"""唯一的 llama.cpp SDK adapter。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from core.exceptions import LlamaCppAdapterError
from core.logger import get_logger


class LlamaCppAdapter:
    """Encapsulate all direct interaction with the llama.cpp Python SDK."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or get_logger(__name__)
        self._model: Any | None = None

    def load_model(self, model_path: str | Path, **kwargs: Any) -> bool:
        """Load a GGUF model, releasing a previously loaded model first."""
        path = Path(model_path)
        if not path.is_file():
            error = LlamaCppAdapterError(f"Model file does not exist: {path}")
            self._logger.error("Unable to load model: %s", error)
            raise error

        self.unload_model()
        try:
            from llama_cpp import Llama

            self._model = Llama(model_path=str(path), **kwargs)
        except Exception as error:
            self._logger.error("Unable to load llama.cpp model %s: %s", path, error)
            self._model = None
            raise LlamaCppAdapterError(f"Unable to load model: {path}") from error
        return True

    def unload_model(self) -> None:
        """Release the current model reference safely."""
        self._model = None

    def is_loaded(self) -> bool:
        """Return whether a model is currently loaded."""
        return self._model is not None

    def generate(self, prompt: str, **kwargs: Any) -> Any:
        """Generate and return the raw llama.cpp response."""
        if self._model is None:
            error = LlamaCppAdapterError("No model is loaded")
            self._logger.error("Unable to generate output: %s", error)
            raise error
        try:
            return self._model(prompt, **kwargs)
        except Exception as error:
            self._logger.error("Unable to generate output: %s", error)
            raise LlamaCppAdapterError("Unable to generate output") from error
