"""项目共用异常。"""


class LlamaCppAdapterError(RuntimeError):
    """llama.cpp Adapter 无法完成操作时抛出。"""


class ModelServiceError(RuntimeError):
    """ModelService 无法完成操作时抛出。"""


class PromptServiceError(RuntimeError):
    """PromptService 无法构建 Prompt 时抛出。"""
