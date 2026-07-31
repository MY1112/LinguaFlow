# M6-002 Settings Information Architecture Refactor


## Reference

读取：

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md

docs/design/assets/linguaFlowDesign.png


## Goal

调整 LinguaFlow Settings 页面结构，使其符合桌面 AI 助手定位。


## 修改文件

src/ui/settings/settings_window.py


## 新增文件

src/ui/settings/pages/selection_page.py

src/ui/settings/pages/ocr_page.py


## 修改文件

src/ui/settings/pages/general_page.py

src/ui/settings/pages/model_page.py

src/ui/settings/pages/shortcut_page.py

src/ui/settings/pages/about_page.py


tests/ui/test_settings_window.py


## 页面结构


SettingsWindow


├── General

│

├── Selection

│

├── Model

│

├── Shortcut

│

├── OCR

│

└── About


## Requirements


# General Page

负责应用级设置：

- 主题切换
- 开机启动
- 关闭到托盘
- Popup显示时间


支持：

System

Light

Dark



# Selection Page

负责划词翻译：

- 开启/关闭划词翻译
- 翻译完成显示Popup
- 默认翻译行为


# Model Page

负责模型信息展示：

- 当前模型名称
- 模型路径
- 加载状态


暂不实现：

- 模型选择
- 模型下载


# Shortcut Page

负责快捷键展示：

当前：

Alt + Q


预留：

- 修改快捷键


# OCR Page

负责OCR能力：

- OCR开关
- OCR快捷键展示
- OCR语言配置占位


暂不接入OCR Engine。


# About Page

展示：

- LinguaFlow名称
- Version
- 技术栈信息


## Rules


禁止：

- 页面直接读写配置文件
- 修改Runtime
- 修改TranslationFeature


保持：

Theme

LFCard

LFButton

已有组件体系。


## Validation


pytest通过

ruff通过

black通过

Settings窗口正常打开

Sidebar切换正常