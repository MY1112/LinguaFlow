# LinguaFlow Layout Implementation Specification

版本：1.0.0

状态：Engineering Implementation Reference

项目：LinguaFlow Desktop Application

------------------------------------------------------------------------

# 1. 文档定位

本文档用于指导 LinguaFlow Desktop UI 工程实现。

本文档不是产品设计说明，不用于重新设计 UI。

唯一视觉基准：

    docs/design/assets/linguaFlowDesign.png

实现目标：

根据设计稿进行工程还原。

禁止：

-   自由发挥 UI 风格
-   使用 Qt 默认控件样式
-   修改已有品牌视觉
-   创建与设计稿不同的信息结构

------------------------------------------------------------------------

# 2. 设计优先级

当不同来源产生冲突时，优先级如下：

1.  linguaFlowDesign.png
2.  Design System 文档
3.  页面 Spec 文档
4.  本实现规范
5.  工程代码现状

------------------------------------------------------------------------

# 3. 工程实现原则

## 3.1 Layout 原则

所有 UI 必须使用 Qt Layout。

推荐：

-   QVBoxLayout
-   QHBoxLayout
-   QGridLayout

禁止：

大量 move(x,y) 或绝对定位。

------------------------------------------------------------------------

## 3.2 组件原则

所有视觉组件必须封装。

禁止直接大量使用：

-   QPushButton
-   QComboBox
-   QTextEdit
-   QLineEdit

必须优先：

-   LFButton
-   LFCard
-   LFInput
-   LFSelect
-   LFStatus
-   LFPopup

------------------------------------------------------------------------

# 4. Global Design Token

## 4.1 Spacing

统一使用 8px Grid。

标准：

  名称   值
  ------ ------
  XS     4px
  SM     8px
  MD     12px
  LG     16px
  XL     24px
  XXL    32px
  Huge   48px

------------------------------------------------------------------------

## 4.2 Radius

组件圆角：

  组件     Radius
  -------- --------
  Button   12px
  Card     16px
  Input    12px
  Popup    16px

------------------------------------------------------------------------

## 4.3 Typography

## Title

用途：

应用标题。

规格：

    font-size:20px
    font-weight:600
    line-height:28px

------------------------------------------------------------------------

## Subtitle

规格：

    font-size:12px
    font-weight:400
    line-height:16px

------------------------------------------------------------------------

## Body

规格：

    font-size:14px
    font-weight:400
    line-height:20px

------------------------------------------------------------------------

# 5. MainWindow

## 5.1 Window

推荐尺寸：

    420px × 620px

属性：

-   Frameless
-   Rounded Corner
-   Light Background
-   Soft Shadow

------------------------------------------------------------------------

# 5.2 MainWindow Layout Tree

    MainWindow

    └── RootContainer

        └── QVBoxLayout

            margin:
            top:20
            left:24
            right:24
            bottom:0


            spacing:16


            ├── Header

            ├── LanguageSelectorArea

            ├── InputCard

            ├── TranslateButtonArea

            ├── ResultCard

            └── StatusBar

------------------------------------------------------------------------

# 6. Header

高度：

    72px

Layout:

    QHBoxLayout

结构：

    Header

    ├── Logo

    └── BrandContainer

        ├── Title

        └── Subtitle

------------------------------------------------------------------------

## Logo

尺寸：

    32px × 32px

来源：

    assets/logo-32.png

------------------------------------------------------------------------

## BrandContainer

Layout：

    QVBoxLayout

Logo 与 Brand：

    12px

------------------------------------------------------------------------

## Title

文本：

    LinguaFlow

规格：

    20px
    600

------------------------------------------------------------------------

## Subtitle

文本：

    Translate Naturally.

规格：

    12px

------------------------------------------------------------------------

# 7. LanguageSelectorArea

高度：

    36px

结构：

    LanguageSelectorArea

    ├── SourceSelector

    ├── SwapButton

    └── TargetSelector

------------------------------------------------------------------------

## Selector

组件：

LFSelect

尺寸：

    150px × 36px

要求：

-   自定义样式
-   圆角
-   Hover 状态
-   Active 状态

禁止：

直接 QComboBox。

------------------------------------------------------------------------

## SwapButton

尺寸：

    40px × 36px

内容：

    ⇄

------------------------------------------------------------------------

# 8. InputCard

组件：

LFCard

尺寸：

    372px × 160px

结构：

    InputCard

    └── InputArea

------------------------------------------------------------------------

## InputArea

组件：

LFInput

要求：

-   多行输入
-   支持字数统计
-   支持快捷键提交

------------------------------------------------------------------------

# 9. Translate Button

组件：

LFButton

尺寸：

    240px × 44px

位置：

水平居中。

内容：

    图片star.png + Translate

状态：

-   Normal
-   Hover
-   Pressed
-   Disabled
-   Loading

------------------------------------------------------------------------

# 10. ResultCard

组件：

LFCard

尺寸：

    372px × 160px

结构：

    ResultCard

    ├── Header

    ├── Content

    └── Actions

------------------------------------------------------------------------

Content：

要求：

-   自动换行
-   支持复制
-   长文本显示

------------------------------------------------------------------------

Actions：

位置：

右下角。

按钮：

-   Copy.png
-   audio.png

------------------------------------------------------------------------

# 11. StatusBar

高度：

40px

结构：

    StatusBar

    ├── ModelStatus

    ├── Spacer

    ├── ModelName

    ├── Spacer

    └── Shortcut

------------------------------------------------------------------------

ModelStatus:

    ● Model Ready

------------------------------------------------------------------------

ModelName:

    Qwen2.5-3B

------------------------------------------------------------------------

Shortcut:

    Alt + Q

------------------------------------------------------------------------

# 12. PopupWindow

## Window

属性：

-   Frameless
-   Always On Top
-   No Taskbar
-   Shadow
-   Rounded Corner

------------------------------------------------------------------------

尺寸：

    360px × 240px

------------------------------------------------------------------------

结构：

    PopupWindow

    ├── Header

    ├── SourceText

    ├── Divider

    ├── TranslationText

    └── ActionBar

------------------------------------------------------------------------

Action:

-   Copy
-   Sound

------------------------------------------------------------------------

# 13. SettingsWindow

结构：

    SettingsWindow

    ├── NavigationPanel

    └── ContentPanel

------------------------------------------------------------------------

Navigation：

宽度：

120px

菜单：

-   通用
-   模型
-   快捷键
-   OCR
-   历史记录
-   关于

------------------------------------------------------------------------

# 14. HistoryWindow

结构：

    HistoryWindow

    ├── SearchBar

    ├── HistoryList

    └── Footer

------------------------------------------------------------------------

HistoryItem：

    HistoryItem

    ├── SourceText

    ├── TargetText

    ├── Time

    └── Favorite

------------------------------------------------------------------------

# 15. TrayMenu

结构：

    TrayMenu

    ├── Logo

    ├── Open MainWindow

    ├── Pause Translation

    ├── Settings

    └── Exit

------------------------------------------------------------------------

# 16. Qt Implementation Mapping

  设计     实现
  -------- -----------------
  Card     QFrame + LFCard
  Button   LFButton
  Select   LFSelect
  Input    LFInput
  Popup    LFPopup
  Status   LFStatus

------------------------------------------------------------------------

# 17. Theme Rules

所有颜色：

必须来自：

    src/ui/theme/theme.py

禁止：

UI 文件中出现：

    #FFFFFF
    #000000
    #xxxxxx

------------------------------------------------------------------------

# 18. 修改边界

允许：

    src/ui/**

谨慎：

    src/app/**

禁止为了 UI 修改：

    src/runtime/**
    src/services/**
    src/features/**

------------------------------------------------------------------------

# 19. Implementation Order

Phase 1:

MainWindow

完成：

-   Header
-   LanguageSelector
-   InputCard
-   TranslateButton
-   ResultCard
-   StatusBar

Phase 2:

PopupWindow

Phase 3:

TrayMenu

Phase 4:

SettingsWindow

Phase 5:

HistoryWindow

------------------------------------------------------------------------

# 20. Acceptance Criteria

视觉：

必须检查：

-   页面比例
-   元素位置
-   间距
-   圆角
-   阴影
-   字体层级
-   Logo 使用

功能：

必须保持：

-   TranslationFeature
-   TranslationWorker
-   HotkeyAdapter
-   SelectionAdapter
-   RuntimeManager
-   ModelService

UI 实现不得破坏已有业务逻辑。

------------------------------------------------------------------------

# End
