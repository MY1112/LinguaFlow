# M6-002 Settings Config Integration


## Goal

将 Settings 页面接入 ConfigService。


## 修改文件

src/ui/settings/pages/*
src/config/*
src/app/application.py


## 新增文件

tests/ui/test_settings_config.py


## Requirements

1. General读取配置

2. Shortcut读取快捷键

3. Selection划词翻译

4. OCR 设置

5. Model显示模型状态

6. About显示版本


## Rules

Settings 页面禁止直接读写配置文件。

必须通过 ConfigService。


## Non Goal

不实现：

- 修改快捷键
- 修改模型
- 开机启动


## Validation

pytest

ruff

black