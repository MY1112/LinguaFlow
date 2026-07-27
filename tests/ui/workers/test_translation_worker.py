"""TranslationWorker 的信号行为测试。"""

from __future__ import annotations

from PySide6.QtCore import QCoreApplication

from ui.workers.translation_worker import TranslationWorker


def test_worker_emits_finished_without_operating_ui() -> None:
    """翻译成功时 Worker 应通过 finished 信号返回结果。"""
    application = QCoreApplication.instance() or QCoreApplication([])
    results: list[str] = []

    class TranslationFeatureStub:
        def translate(self, text: str, source_language: str, target_language: str) -> str:
            return f"{text}:{source_language}->{target_language}"

    worker = TranslationWorker(TranslationFeatureStub(), "Hello", "中文", "英文")
    worker.finished.connect(results.append)

    worker.run()
    application.processEvents()

    assert results == ["Hello:中文->英文"]


def test_worker_emits_failed_without_operating_ui() -> None:
    """翻译失败时 Worker 应通过 failed 信号返回错误。"""
    application = QCoreApplication.instance() or QCoreApplication([])
    errors: list[str] = []

    class TranslationFeatureStub:
        def translate(self, text: str, source_language: str, target_language: str) -> str:
            raise RuntimeError("模型未加载")

    worker = TranslationWorker(TranslationFeatureStub(), "Hello", "中文", "英文")
    worker.failed.connect(errors.append)

    worker.run()
    application.processEvents()

    assert errors == ["模型未加载"]
