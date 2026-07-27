# LinguaFlow Component Specification v1.0


# 1. 组件设计原则


LinguaFlow 所有 UI 必须基于公共组件。


禁止：

- 页面内直接定义视觉样式
- 重复创建相似组件
- 自定义颜色
- 自定义间距


所有组件：

继承：

20-Design-System.md



--------------------------------------------------


# 2. Component目录规范


UI组件目录：


src/ui/components/


结构：


components/

├── lf_button.py

├── lf_card.py

├── lf_input.py

├── lf_select.py

├── lf_status.py

├── lf_popup.py

├── lf_toast.py

└── lf_icon.py



命名规则：

LinguaFlow 前缀：

LF



--------------------------------------------------


# 3. LFButton


用途：

统一按钮。


替代：

QPushButton



## 类型


Primary

Secondary

Danger

Ghost



--------------------------------------------------


## Primary Button


用途：

主要操作。


例如：

Translate


规格：


高度：

42px


圆角：

999px


Padding：

20px 32px



样式：


背景：

Primary


文字：

White



Hover：

Primary Hover



Disabled：

Opacity 0.5



--------------------------------------------------


## Secondary Button


用途：

辅助操作。


例如：

复制


样式：


背景：

White


Border:

Border


文字：

Text



--------------------------------------------------


## Danger Button


用途：

危险操作。


例如：

删除模型



背景：

Error



--------------------------------------------------


# 4. LFCard


用途：

所有内容容器。



替代：

QFrame



规格：


Background：

Surface


Radius：

16px


Padding：

24px


Border：

1px Border



Shadow：

Card Shadow



--------------------------------------------------


# 5. LFInput


用途：

统一输入框。


替代：

QLineEdit

QTextEdit



--------------------------------------------------


## TextInput


高度：

42px



样式：


Background:

White


Radius:

12px


Border:

Border



Focus：

Primary Border



--------------------------------------------------


## TextArea


用途：

翻译输入。


高度：

160px



支持：

- placeholder
- 字数统计
- 最大长度


--------------------------------------------------


# 6. LFSelect


用途：

选择器。


例如：

语言选择。


规格：


高度：

42px


宽度：

150px



样式：


Card 风格。



Radius：

12px



--------------------------------------------------


# 7. LFIcon


用途：

统一图标。


来源：


Fluent Icon Style



要求：

- 线性
- 圆角
- 简洁



禁止：

混用：

Material Icon

FontAwesome

Emoji



--------------------------------------------------


# 8. LFStatus


用途：

状态展示。



场景：


模型状态


翻译状态


系统状态



结构：


● 状态点

+

文字



--------------------------------------------------


## Success


示例：


● Model Ready



颜色：

Success



--------------------------------------------------


## Loading


示例：


● Translating...



颜色：

Primary



--------------------------------------------------


## Error


示例：


● Model Error



颜色：

Error



--------------------------------------------------


# 9. LFToast


用途：

短消息提示。



替代：

QMessageBox



原则：

不打断用户。



--------------------------------------------------


## Success Toast


例如：


复制成功



显示：

2秒



--------------------------------------------------


## Error Toast


例如：


翻译失败，请重试



显示：

3秒



--------------------------------------------------


禁止：

显示：

Traceback

Python异常

文件路径



--------------------------------------------------


# 10. LFPopup


用途：

快捷翻译结果窗口。



要求：


继承：

23-PopupWindow-Spec



统一：


Radius:

16px


Shadow:

Popup Shadow



--------------------------------------------------


# 11. LFLoading


用途：

耗时状态。


场景：

模型加载

翻译中



样式：

轻量动画。



禁止：

大面积 Loading 页面。



--------------------------------------------------


# 12. LFEmptyState


用途：

空状态。



例如：


没有历史记录。



结构：


Icon


Title


Description



示例：


暂无翻译记录

你的翻译历史会显示在这里。



--------------------------------------------------


# 13. 组件状态规范


所有交互组件必须支持：


Normal


Hover


Pressed


Disabled


Loading



--------------------------------------------------


# 14. 动画规范


统一：


Fast:

150ms


Normal:

200ms


Slow:

300ms



用途：


按钮反馈：

150ms


Popup：

200ms


页面切换：

300ms



--------------------------------------------------


# 15. 开发规则


新增组件必须：


1. 判断是否已有组件

2. 更新本文档

3. 再开发



禁止：

临时组件。



--------------------------------------------------


# 16. 当前实现优先级


第一阶段：


必须实现：


LFButton

LFCard

LFInput

LFSelect

LFStatus

LFToast



第二阶段：


LFPopup

LFLoading

LFEmptyState



第三阶段：

动画系统。


