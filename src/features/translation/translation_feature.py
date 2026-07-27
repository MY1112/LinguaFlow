"""文本翻译 Feature。"""

from __future__ import annotations

import logging

from core.exceptions import ModelServiceError, PromptServiceError
from core.logger import get_logger
from services.model_service import ModelService
from services.prompt_service import PromptService


class TranslationError(RuntimeError):
    """翻译 Feature 无法完成翻译时抛出。"""


class TranslationFeature:
    """协调 PromptService 和 ModelService 完成文本翻译。"""

    def __init__(
        self,
        prompt_service: PromptService | None = None,
        model_service: ModelService | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or get_logger(__name__)
        self._prompt_service = prompt_service or PromptService(self._logger)
        self._model_service = model_service or ModelService(self._logger)

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """校验输入并返回翻译结果。"""
        self._validate_input(text, source_language, target_language)
        self._logger.info(
            "开始翻译，输入长度：%d，源语言：%s，目标语言：%s",
            len(text),
            source_language,
            target_language,
        )
        try:
            prompt = self._prompt_service.build_translate_prompt(
                text,
                source_language,
                target_language,
            )
            result = self._model_service.generate(prompt)
        except (PromptServiceError, ModelServiceError) as error:
            self._logger.error("翻译异常：%s", error)
            raise TranslationError("翻译失败") from error
        except Exception as error:
            self._logger.error("翻译发生未预期异常：%s", error)
            raise TranslationError("翻译失败") from error

        if not isinstance(result, str):
            error = TranslationError("翻译结果不是字符串")
            self._logger.error("翻译异常：%s", error)
            raise error
        self._logger.info("翻译完成，结果长度：%d", len(result))
        return result

    def _validate_input(self, text: str, source_language: str, target_language: str) -> None:
        if not isinstance(text, str) or not text.strip():
            raise TranslationError("输入内容不能为空")
        if not isinstance(source_language, str) or not source_language.strip():
            raise TranslationError("源语言不能为空")
        if not isinstance(target_language, str) or not target_language.strip():
            raise TranslationError("目标语言不能为空")
        if source_language.strip() == target_language.strip():
            raise TranslationError("源语言和目标语言不能相同")
