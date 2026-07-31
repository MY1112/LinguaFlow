# M5-003 Selection Stability + Tray Menu Enhancement


## Reference

读取：

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md

docs/design/assets/linguaFlowDesign.png


## Goal

提升划词翻译稳定性，并重构系统托盘菜单。


## Scope

允许修改：

src/ui/**
src/integrations/**
src/app/application.py


禁止修改：

src/features/**
src/services/**
src/runtime/**


## Requirements


### Selection

1. 增强选中文本获取

2. 支持空文本状态

3. 增加日志

4. 保证剪贴板恢复


### Tray

1. 新增 LFTrayMenu

2. 使用 LinguaFlow 视觉规范

3. 增加：

- LinguaFlow
- 打开主窗口
- 暂停划词翻译
- 设置
- 退出


4. 保持托盘生命周期


## Acceptance

pytest通过

ruff通过

black通过

Alt+Q流程正常

Tray菜单正常