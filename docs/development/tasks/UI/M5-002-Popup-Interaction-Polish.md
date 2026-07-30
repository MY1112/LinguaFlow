# M5-002 Popup Interaction Polish


## Reference

读取：

docs/design/23-PopupWindow-Spec.md

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md


## Goal

优化 Popup 翻译交互体验。


## Scope

允许：

src/ui/**
src/app/application.py


禁止：

src/runtime/**
src/services/**
src/features/**


## Requirements


1. 增加 Popup Loading 状态

2. 翻译开始立即显示 Popup

3. 翻译完成替换内容

4. 增加失败状态

5. Retry重新触发翻译


## Keep

保持：

Alt+Q流程

TranslationWorker

TranslationFeature


## Acceptance

pytest通过

ruff通过

black通过

真实 Alt+Q 流程可用