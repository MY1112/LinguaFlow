# LinguaFlow

LinguaFlow 是一个基于 Python、PySide6 和 llama.cpp 的本地 AI 翻译桌面工具。

它优先在本机运行 GGUF 大语言模型，支持普通文本翻译，也支持通过全局快捷键快速翻译其他应用中的选中文本。翻译结果会以轻量 Popup 窗口显示，应用可以缩小到系统托盘并保持后台运行。

## 当前能力

- 本地 GGUF 模型加载与文本推理
- 中文与英文之间的文本翻译
- 主窗口文本翻译
- `Alt + Q` 全局划词翻译
- 自动读取选中文本并恢复原剪贴板内容
- 翻译 Popup 窗口
  - 显示原文与译文
  - 加载、成功、失败状态
  - 失败后重试
  - 复制译文
  - 原文和译文音频按钮入口
- 系统托盘操作
  - Open
  - Translate Selection
  - Pause / Resume
  - Settings 入口
  - About 入口
  - Exit
- 主窗口关闭后隐藏到系统托盘
- 托盘右键打开和双击恢复主窗口
- 全局统一滚动条与基础 UI 样式
- 文件日志和 JSON 配置

## 运行环境

- Windows 10 或 Windows 11
- Python 3.12 或更高版本
- PySide6
- llama-cpp-python
- 可用的 GGUF 模型文件

项目依赖建议安装在项目虚拟环境中。不要使用系统 Python 作为依赖判断依据。

## 安装

在项目根目录创建并激活虚拟环境：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

安装运行依赖：

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

安装开发依赖：

```powershell
python -m pip install -e .[dev]
```

如果 PowerShell 阻止脚本执行，可以使用虚拟环境中的 Python 直接运行：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

## 模型配置

默认配置文件为 `config/settings.json`：

```json
{
  "app": {
    "name": "LinguaFlow",
    "model_path": "models/qwen2.5-3b-instruct-q4_k_m.gguf"
  }
}
```

将 GGUF 模型放入 `models/` 目录，并让 `app.model_path` 指向实际文件。

相对路径以项目根目录为基准，也可以配置绝对路径：

```json
{
  "app": {
    "model_path": "D:/models/qwen2.5-3b-instruct-q4_k_m.gguf"
  }
}
```

应用启动时会尝试加载配置中的模型。如果模型路径不存在或模型加载失败，应用仍会启动，但翻译功能无法正常工作；具体原因会写入 `logs/`。

## 启动应用

确保虚拟环境已激活后，在项目根目录执行：

```powershell
python -m src.main
```

也可以显式使用虚拟环境解释器：

```powershell
.\.venv\Scripts\python.exe -m src.main
```

## 基本使用

### 主窗口翻译

1. 启动 LinguaFlow。
2. 在输入框中输入文本。
3. 选择源语言和目标语言。
4. 点击 `Translate`，或使用 `Ctrl + Enter`。
5. 在结果区域查看并复制译文。

### 划词翻译

1. 在任意支持文本选择的应用中选中文本。
2. 按下 `Alt + Q`。
3. LinguaFlow 会读取选中文本并启动后台翻译。
4. 翻译结果会显示在 Popup 窗口中。

划词翻译会临时使用剪贴板读取选中文本，完成后会恢复原剪贴板内容。没有有效选中文本时，流程会记录日志并结束，不会启动翻译任务。

### 系统托盘

关闭主窗口时，LinguaFlow 会隐藏到系统托盘而不是直接退出。

- 右键托盘图标，选择 `Open` 恢复主窗口。
- 双击托盘图标恢复主窗口。
- 使用 `Pause` 暂停全局划词翻译快捷键，使用 `Resume` 恢复。
- 选择 `Exit` 完全退出应用。

## 配置与日志

```text
config/
├─ settings.json    应用设置和模型路径
└─ hotkey.json      快捷键配置

logs/               按日期生成的应用日志
models/             本地 GGUF 模型目录
```

配置服务使用 JSON 文件保存设置。日志统一写入 `logs/`，包括模型加载、翻译、划词捕获和异常信息。

## 项目结构

```text
src/
├─ app/             应用生命周期与启动协调
├─ core/            日志和基础异常
├─ features/        业务 Feature，例如翻译
├─ integrations/    llama.cpp、剪贴板、快捷键等系统集成
├─ runtime/         Runtime 和模型运行状态
├─ services/        配置、模型、Prompt 等公共服务
├─ ui/              主窗口、Popup、托盘和 UI 组件
└─ main.py          Windows 应用入口

tests/              自动化测试
docs/               架构、设计和开发任务文档
assets/              Logo、图标等项目资源
```

项目遵循 Local First 和 Feature First 原则：核心 AI 能力默认在本地运行，业务能力集中在 Feature 中，第三方库通过 `integrations/` 统一封装。

## 开发与验证

激活虚拟环境后运行测试：

```powershell
python -m pytest -q
```

运行 Ruff：

```powershell
ruff check src tests
```

检查 Black 格式：

```powershell
black --check src tests
```

格式化代码：

```powershell
black src tests
```

涉及 Qt 界面测试时，可在无窗口环境中执行：

```powershell
$env:QT_QPA_PLATFORM = "offscreen"
python -m pytest -q
```

## 当前限制

- 当前版本主要面向 Windows。
- 当前翻译流程依赖本地 llama.cpp 和可用的 GGUF 模型。
- 当前 UI 主要覆盖文本翻译和划词翻译，OCR、截图翻译等模块尚未接入完整用户流程。
- Tray 中的 Settings 和 About 目前保留为入口，具体窗口功能将在后续任务中接入。
- 音频按钮目前是 UI 入口，音频生成与播放能力尚未作为完整功能交付。

## 文档入口

- [开发原则](docs/architecture/00-开发原则.md)
- [产品需求](docs/architecture/01-产品需求（PRD）.md)
- [工程架构](docs/architecture/02-工程架构.md)
- [项目结构](docs/architecture/03-项目结构.md)
- [开发规范](docs/architecture/04-开发规范.md)
- [开发任务](docs/development/tasks/)

## 许可证

项目许可证尚未确定。