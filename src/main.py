"""LinguaFlow application entry point."""

from __future__ import annotations

from app.windows_identity import set_app_user_model_id


def main() -> int:
    """Set the Windows identity before creating the Qt application."""
    set_app_user_model_id()
    from app.application import Application

    return Application().run()


if __name__ == "__main__":
    raise SystemExit(main())
