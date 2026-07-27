# M4-004 MainWindow UI Implementation


## Reference

必须读取：

docs/design/assets/linguaFlowDesign.png

docs/design/26-LinguaFlow-Layout-Implementation-Spec.md


## Goal

严格还原 MainWindow UI。


## Scope

允许修改：

src/ui/**


禁止修改：

src/runtime/**
src/services/**
src/features/**
src/integrations/**


## Requirements

1. 重构 MainWindow Layout

2. 创建 Header Component

3. 创建 Select Component

4. 完善 InputCard

5. 完善 ResultCard

6. 完善 StatusBar

7. 保持 TranslationFeature 调用链不变


## Acceptance

pytest通过

ruff通过

black通过

应用正常启动