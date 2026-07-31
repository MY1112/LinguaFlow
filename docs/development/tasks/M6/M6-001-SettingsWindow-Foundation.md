# M6-001 SettingsWindow Foundation


## Reference

读取：

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md


## Goal

实现 LinguaFlow Settings 基础窗口。


# 修改文件

src/app/application.py

src/ui/tray.py


# 新增文件

src/ui/settings/__init__.py

src/ui/settings/settings_window.py

src/ui/settings/pages/__init__.py

src/ui/settings/pages/general_page.py

src/ui/settings/pages/selection_page.py

src/ui/settings/pages/model_page.py

src/ui/settings/pages/shortcut_page.py

src/ui/settings/pages/ocr_page.py

src/ui/settings/pages/about_page.py

tests/ui/test_settings_window.py


# Requirements


## SettingsWindow

创建 SettingsWindow：

尺寸：

720 × 520


结构：

SettingsWindow

├── Sidebar

│
├── General

├── Shortcut

├── Selection

├── OCR

├── Model

└── About

│

└── ContentArea


使用：

LFCard

LFButton

Theme


## Sidebar

实现页面切换。


## Tray Integration

点击 Tray -> Settings：

打开 SettingsWindow。


## Non Goal

本 Task 不实现：

- 配置保存
- 快捷键修改
- 模型切换
- 开机启动


## Validation

pytest

ruff

black

应用启动正常

Tray Settings入口正常