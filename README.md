# LinguaFlow

LinguaFlow 是一个 Local First 的 Windows 桌面 AI 工具。目前项目处于 Bootstrap 阶段，仅提供可启动的 PySide6 空窗口、统一日志、配置服务和运行上下文。

## 环境要求

- Windows 10 或 Windows 11
- Python 3.11+

## 安装

在项目根目录执行：

```powershell
python -m pip install -e .
```

## 启动

```powershell
python src/main.py
```

启动后会显示 LinguaFlow 空主窗口。关闭窗口即可正常退出。

## 当前范围

当前版本不包含翻译、OCR、快捷键、模型加载或其他业务功能。配置文件位于 `config/`，日志由统一 Logger 写入 `logs/`。
