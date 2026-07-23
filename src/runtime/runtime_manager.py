"""AI runtime lifecycle management."""

from __future__ import annotations

import logging

from core.logger import get_logger
from runtime.runtime_state import RuntimeState
from services.model_service import ModelService


class RuntimeManager:
    """Initialize and release the model-independent AI runtime."""

    def __init__(
        self,
        logger: logging.Logger | None = None,
        model_service: ModelService | None = None,
    ) -> None:
        self._logger = logger or get_logger(__name__)
        self._model_service = model_service or ModelService(self._logger)
        self._state = RuntimeState()

    def initialize(self) -> None:
        """Initialize the AI runtime framework without loading a model."""
        if self._state.initialized:
            return
        self._state.initialized = True
        self._logger.info("AI Runtime initialized")

    def shutdown(self) -> None:
        """Release model resources and shut down the AI runtime framework."""
        self._model_service.unload_model()
        if not self._state.initialized:
            return
        self._state = RuntimeState()
        self._logger.info("AI Runtime released")

    def get_state(self) -> RuntimeState:
        """Return the current runtime state."""
        return self._state
