"""LinguaFlow 应用程序入口。"""

from __future__ import annotations

from app.application import Application


def main() -> int:
    """运行桌面应用程序。"""
    return Application().run()


if __name__ == "__main__":
    raise SystemExit(main())
