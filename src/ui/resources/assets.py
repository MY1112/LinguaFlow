"""统一管理 UI 静态资源。"""

from __future__ import annotations

from pathlib import Path

_SUPPORTED_LOGO_SIZES = (16, 32, 512)


def get_logo(size: int) -> Path:
    """返回指定尺寸的 Logo 资源路径。"""
    if size not in _SUPPORTED_LOGO_SIZES:
        supported_sizes = ", ".join(str(value) for value in _SUPPORTED_LOGO_SIZES)
        raise ValueError(f"Logo 尺寸必须是 {supported_sizes}")

    project_root = Path(__file__).resolve().parents[3]
    return project_root / "assets" / f"logo_{size}.png"
