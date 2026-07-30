"""M5-003 SelectionAdapter 回归测试。"""

from __future__ import annotations

from integrations.selection import SelectionAdapter


def test_selection_capture_does_not_overwrite_clipboard_when_snapshot_fails(monkeypatch) -> None:
    """无法读取原剪贴板时不得用空值覆盖用户剪贴板。"""
    adapter = SelectionAdapter()
    writes: list[str] = []

    monkeypatch.setattr("integrations.selection.sys.platform", "win32")
    monkeypatch.setattr(
        adapter,
        "_read_clipboard_text",
        lambda: (_ for _ in ()).throw(OSError("busy")),
    )
    monkeypatch.setattr(adapter, "_write_clipboard_text", writes.append)

    assert adapter.get_selected_text() == ""
    assert writes == []
