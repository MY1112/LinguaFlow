# LinguaFlow MainWindow Specification v1.0


# 1. 页面定位


MainWindow 是 LinguaFlow 的核心工作界面。


用户打开应用后：

第一目标：

完成一次翻译。


首页只展示：

- 输入
- 翻译方向
- 翻译结果
- 当前状态


隐藏复杂能力：

- 模型管理
- Prompt
- OCR
- 历史记录
- 高级参数


这些功能进入 Settings。



--------------------------------------------------


# 2. 窗口规格


窗口名称：

LinguaFlow


默认尺寸：

760 × 620 px


最小尺寸：

640 × 520 px


窗口行为：

支持：

- 最大化
- 最小化
- 关闭隐藏到托盘


禁止：

关闭直接退出程序。



窗口背景：

#F7F8FA



--------------------------------------------------


# 3. 整体布局


采用垂直布局。


结构：


Window


├── Header

│

├── Language Selector

│

├── Input Card

│

├── Translate Button

│

├── Result Card

│

└── Status Bar



布局间距：

统一使用：

8pt Grid



主要间距：

24px



--------------------------------------------------


# 4. Header


高度：

72px



布局：

左侧：

Logo + 产品信息



右侧：

窗口控制按钮



结构：


[Logo 32px]


LinguaFlow

Translate Naturally.






## Logo


尺寸：

32 × 32 px


来源：

assets/logo



禁止：

重新绘制 Logo。



---

## 产品名称


文字：

LinguaFlow


字号：

20px


字重：

600


颜色：

#1A1D23



---

## Slogan


文字：

Translate Naturally.


字号：

12px


颜色：

#6B7280



--------------------------------------------------


# 5. Language Selector


位置：

Header 下方



高度：

48px



结构：


Source Language


↓

Swap Button


↓

Target Language



布局：

横向排列。


示例：


中文       ⇄       English



--------------------------------------------------


# Language Select 控件


尺寸：

150 × 42 px



样式：

Card 风格。



背景：

White



Radius：

12px



Border：

#E9EDF3



文字：

14px



支持：

点击展开语言列表。



当前版本：

仅支持：

中文

English



未来扩展：

日语

韩语

法语

德语



--------------------------------------------------


# Swap Button


尺寸：

42 × 42 px



样式：

圆形按钮。



默认：

White



Icon：

交换箭头。



Hover：

Primary 浅色背景。



功能：

交换源语言和目标语言。



--------------------------------------------------


# 6. Input Card


用途：

用户输入文本。



尺寸：

宽度：

填满窗口。



高度：

180px



样式：


Card


Background:

White


Radius:

16px


Padding:

20px



--------------------------------------------------


# Input TextArea


Placeholder:


请输入想翻译的内容...



字号：

14px



最大字符：

5000



右下角显示：

当前字数 / 最大字数



例如：

0 / 5000



--------------------------------------------------


# 输入状态


## Empty


显示 Placeholder。



## Focus


Border:

Primary



## Typing


正常状态。



## Too Long


显示错误提示。



--------------------------------------------------


# 7. Translate Button


位置：

输入区域下方。



尺寸：

120 × 42 px



水平居中。



样式：

Primary Button



文字：

Translate



Icon:

可选 Sparkle Icon。



--------------------------------------------------


# Button 状态


## Normal


可点击。



## Loading


显示：

翻译中...



禁止重复点击。



## Disabled


灰色。



--------------------------------------------------


# 8. Result Card


用途：

显示翻译结果。


尺寸：

180px



样式：

Card



--------------------------------------------------


内容结构：


标题：

Translation Result



正文：

翻译结果文本



底部：

操作按钮



包括：

复制

朗读



--------------------------------------------------


# Result 状态


## Empty


显示：

翻译结果将在这里显示...



## Success


显示翻译内容。



## Error


显示友好错误。


例如：

翻译失败，请稍后重试。



禁止显示：

Python异常。

Trace信息。



--------------------------------------------------


# 9. Status Bar


位置：

窗口底部。



高度：

40px



背景：

透明。



内容：


左侧：


绿色状态点


Model Ready



模型名称：

Qwen2.5-3B



右侧：


快捷键：

Alt + Q



设置按钮：

⚙



帮助按钮：

?



--------------------------------------------------


# 状态样式


正常：


● Model Ready


颜色：

Success



加载中：


● Loading Model



错误：


● Model Error



颜色：

Error



--------------------------------------------------


# 10. 交互规则


## 打开应用


自动：

- 初始化 Runtime
- 加载模型
- 显示状态



---

## 点击翻译


流程：

输入检查

↓

TranslationFeature

↓

ModelService

↓

显示结果



---

## Ctrl + Enter


支持快捷翻译。


---

## Esc


关闭 Popup。


MainWindow：

不退出。


--------------------------------------------------


# 11. 不允许


MainWindow 禁止加入：


- Token显示
- Prompt编辑
- Temperature
- Top_p
- 模型路径
- Debug日志


这些属于高级设置。


--------------------------------------------------


# 12. 开发要求


实现必须遵循：


20-Design-System.md


21-Brand-Identity.md



不得自行：

- 修改颜色
- 修改圆角
- 增加组件
- 改变布局结构


新增需求必须先更新设计文档。

