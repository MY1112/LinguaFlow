"""State container for the AI runtime."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class RuntimeState:
    """Runtime state without model or business-specific data."""

    initialized: bool = False
    model_loaded: bool = False
    current_model_path: Path | None = None
