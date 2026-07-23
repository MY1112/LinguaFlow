from pathlib import Path

from llama_cpp import Llama

MODEL = Path("models/qwen2.5-3b-instruct-q4_k_m.gguf")

print("开始加载模型...")

llm = Llama(
    model_path=str(MODEL),
    n_ctx=2048,
    n_threads=8,      # 可以根据 CPU 调整
    verbose=False,
)

print("模型加载完成！")

response = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "你是一名专业翻译助手。"
        },
        {
            "role": "user",
            "content": "请把 Hello World 翻译成中文，只输出翻译结果。"
        }
    ],
    max_tokens=64,
    temperature=0.2,
)

print("模型回复：")
print(response["choices"][0]["message"]["content"])