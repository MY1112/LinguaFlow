"""Centralized application logging."""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(log_directory: Path, level: int = logging.INFO) -> logging.Logger:
    """Configure and return the application logger."""
    log_directory.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("linguaflow")
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler = logging.FileHandler(
        log_directory / f"{date.today().isoformat()}.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a child logger after application logging has been configured."""
    return logging.getLogger("linguaflow" if not name else f"linguaflow.{name}")
