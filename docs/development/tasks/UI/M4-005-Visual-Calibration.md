# M4-005 Visual Calibration


## Reference

必须读取：

docs/design/assets/linguaFlowDesign.png

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md


## Goal

根据设计图进行 MainWindow 第一轮视觉校准。


## Scope

允许：

src/ui/**


禁止：

src/runtime/**
src/services/**
src/features/**


## Requirements

检查并调整：

1. Window尺寸
2. Header间距
3. Card尺寸
4. Button尺寸
5. Font层级
6. Padding
7. Radius
8. Shadow
9. Color


禁止改变：

TranslationFeature

TranslationWorker

快捷键流程


## Acceptance

pytest通过

ruff通过

black通过

应用启动正常

人工截图与设计稿接近