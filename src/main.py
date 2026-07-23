"""LinguaFlow application entry point."""

from __future__ import annotations

from app.application import Application


def main() -> int:
    """Run the desktop application."""
    return Application().run()


if __name__ == "__main__":
    raise SystemExit(main())
