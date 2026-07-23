"""应用生命周期共享上下文。"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from runtime.runtime_manager import RuntimeManager
from services.config_service import ConfigService
from services.prompt_service import PromptService


@dataclass
class AppContext:
    """维护应用运行所需的共享对象。"""

    logger: logging.Logger
    config_service: ConfigService
    runtime: RuntimeManager
    prompt_service: PromptService
