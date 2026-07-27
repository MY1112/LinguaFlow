"""UI 资源管理测试。"""

from pathlib import Path

import pytest

from ui.resources.assets import get_logo


@pytest.mark.parametrize("size", [16, 32, 512])
def test_get_logo_returns_existing_logo_asset(size: int) -> None:
    """get_logo 应返回指定尺寸的现有 Logo 文件。"""
    logo = get_logo(size)

    assert isinstance(logo, Path)
    assert logo.name == f"logo_{size}.png"
    assert logo.is_file()


def test_get_logo_rejects_unsupported_size() -> None:
    """get_logo 对未提供的尺寸应明确报错。"""
    with pytest.raises(ValueError, match="16, 32, 512"):
        get_logo(64)
