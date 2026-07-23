# LinguaFlow

LinguaFlow 是一个基于 Python、PySide6 和 llama.cpp 的 Local First 本地 AI 桌面工具。

当前项目处于 Milestone 1 基础设施阶段，仅提供统一日志、配置服务、运行时上下文和空白主窗口，不包含翻译、OCR、快捷键或模型加载功能。

## 快速启动

```powershell
python -m pip install -e .
python -m src.main
```

关闭主窗口即可退出程序。

## 项目目录

```text
config/       用户配置
docs/         项目文档
logs/         Logger 输出
models/       本地模型目录
resources/    公共资源
src/          Python 源码
tests/        测试目录（按需建立）
```

## 文档入口

- [开发原则](docs/architecture/00-开发原则.md)
- [产品需求](docs/architecture/01-产品需求（PRD）.md)
- [工程架构](docs/architecture/02-工程架构.md)
- [项目结构](docs/architecture/03-项目结构.md)
- [开发规范](docs/architecture/04-开发规范.md)
- [开发任务](docs/development/tasks/)
