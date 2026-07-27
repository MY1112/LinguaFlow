"""翻译后台 Worker。"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from features.translation.translation_feature import TranslationFeature


class TranslationWorker(QObject):
    """在线程中调用 TranslationFeature 执行翻译。"""

    finished = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        translation_feature: TranslationFeature,
        text: str,
        source_language: str,
        target_language: str,
    ) -> None:
        super().__init__()
        self._translation_feature = translation_feature
        self._text = text
        self._source_language = source_language
        self._target_language = target_language

    @Slot()
    def run(self) -> None:
        """执行翻译并通过信号返回结果。"""
        try:
            result = self._translation_feature.translate(
                self._text,
                self._source_language,
                self._target_language,
            )
        except Exception as error:
            self.failed.emit(str(error))
            return
        self.finished.emit(result)
