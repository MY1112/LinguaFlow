# M5-001 PopupWindow Implementation


## Reference

必须读取：

docs/design/assets/linguaFlowDesign.png

docs/design/23-PopupWindow-Spec.md

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md


## Goal

实现 LinguaFlow 翻译结果 Popup。


## Scope

允许：

src/ui/**

src/app/application.py


禁止：

src/runtime/**

src/services/**

src/features/**


## Requirements

1. 重构 PopupWindow

2. 使用 LFCard 风格

3. 实现 Header

4. 实现原文区域

5. 实现译文区域

6. 实现 Copy/Sound

7. 保持 Alt+Q 翻译链路


## Acceptance

pytest通过

ruff通过

black通过

Popup显示正常

不会阻塞主窗口