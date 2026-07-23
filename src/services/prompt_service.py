"""统一管理 Prompt 模板。"""

from __future__ import annotations

import logging
from typing import Final

from core.exceptions import PromptServiceError
from core.logger import get_logger


class PromptService:
    """集中构建当前阶段支持的中英文翻译 Prompt。"""

    _PROMPT_TEMPLATE: Final[str] = """你是一名专业翻译助手。

请将下面内容从{source_language}翻译为{target_language}。

要求：
1. 保持原意。
2. 保持语气。
3. 不添加解释。
4. 仅输出翻译结果。

内容：
{text}"""

    _LANGUAGE_ALIASES: Final[dict[str, str]] = {
        "中文": "中文",
        "Chinese": "中文",
        "chinese": "中文",
        "zh": "中文",
        "zh-CN": "中文",
        "英文": "英文",
        "English": "英文",
        "english": "英文",
        "en": "英文",
        "en-US": "英文",
    }

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or get_logger(__name__)

    def build_translate_prompt(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """根据语言方向和原文构建最终翻译 Prompt。"""
        try:
            source = self._normalize_language(source_language)
            target = self._normalize_language(target_language)
            self._validate_text(text)
            self._validate_direction(source, target)
            prompt = self._PROMPT_TEMPLATE.format(
                source_language=source,
                target_language=target,
                text=text,
            )
        except PromptServiceError as error:
            self._logger.error("Prompt 构建异常：%s", error)
            raise
        self._logger.info("Prompt 构建完成，类型：%s→%s", source, target)
        return prompt

    def _normalize_language(self, language: str) -> str:
        if not isinstance(language, str):
            raise PromptServiceError("语言参数必须是字符串")
        normalized = self._LANGUAGE_ALIASES.get(language)
        if normalized is None:
            raise PromptServiceError(f"暂不支持的语言：{language}")
        return normalized

    def _validate_text(self, text: str) -> None:
        if not isinstance(text, str):
            raise PromptServiceError("待翻译文本必须是字符串")

    def _validate_direction(self, source: str, target: str) -> None:
        if (source, target) not in {("中文", "英文"), ("英文", "中文")}:
            raise PromptServiceError(f"暂不支持的翻译方向：{source}→{target}")
