"""Windows shell identity helpers."""

from __future__ import annotations

import sys

APP_USER_MODEL_ID = "LinguaFlow.Desktop"


def set_app_user_model_id() -> None:
    """Set the stable Windows identity used for taskbar grouping and icons."""
    if sys.platform != "win32":
        return

    import ctypes

    result = ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
    if result != 0:
        raise OSError(f"SetCurrentProcessExplicitAppUserModelID failed: 0x{result:08X}")
