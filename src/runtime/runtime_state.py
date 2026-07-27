"""AI Runtime 状态容器。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class RuntimeState:
    """不包含模型或业务专属数据的 Runtime 状态。"""

    initialized: bool = False
    model_loaded: bool = False
    current_model_path: Path | None = None
