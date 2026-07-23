"""Shared runtime context for the application lifecycle."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from services.config_service import ConfigService


@dataclass
class AppContext:
    """Container for shared runtime dependencies."""

    logger: logging.Logger
    config_service: ConfigService
