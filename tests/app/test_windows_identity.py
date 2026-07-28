"""Windows taskbar identity tests."""

from __future__ import annotations

import ctypes

from app.windows_identity import APP_USER_MODEL_ID, set_app_user_model_id


def test_sets_explicit_windows_app_user_model_id() -> None:
    """The process should expose the stable LinguaFlow taskbar identity."""
    set_app_user_model_id()

    value = ctypes.c_wchar_p()
    result = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID(ctypes.byref(value))

    assert result == 0
    assert value.value == APP_USER_MODEL_ID
