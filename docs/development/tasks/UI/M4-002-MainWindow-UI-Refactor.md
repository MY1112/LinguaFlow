# M4-002 MainWindow UI Refactor


## Task ID

M4-002


## Task目标


按照 LinguaFlow UI Design 规范，实现 MainWindow 产品化 UI。


本 Task 的设计依据：

- docs/design/20-Design-System.md
- docs/design/21-Brand-Identity.md
- docs/design/22-MainWindow-Spec.md
- docs/design/25-Component-Spec.md


以上 Design 文档为唯一视觉规范来源。


如果 Task 描述与 Design 文档冲突：

以 Design 文档为准。


---

# 修改范围


## 修改文件


src/ui/main_window.py



---

## 新增文件


src/ui/components/lf_button.py

src/ui/components/lf_card.py

src/ui/components/lf_input.py

src/ui/components/lf_status.py



---

# 实现目标


## MainWindow


根据：

docs/design/22-MainWindow-Spec.md


实现完整主窗口布局。


包括：

- Header
- 翻译主体区域
- 状态区域


具体：

- 尺寸
- 间距
- 颜色
- 字体
- 布局方式

全部遵循 Design 文档。



---

# 公共组件


根据：

docs/design/25-Component-Spec.md


实现 UI 公共组件。


包含：


## LFButton


职责：

统一按钮组件。


基于 Qt QPushButton。


---


## LFCard


职责：

统一卡片容器组件。


基于 Qt QFrame。


---


## LFInput


职责：

统一文本输入组件。


基于 Qt 文本输入控件。


---


## LFStatus


职责：

统一状态展示组件。



---

# Theme 使用要求


所有 UI 实现必须使用：

src/ui/theme/theme.py


src/ui/styles/stylesheet.py



禁止：

- 在 UI 页面中新增颜色常量
- 在 UI 页面中新增尺寸常量
- 重复定义 Design 参数


---

# 功能保持


必须保持现有功能：

- 翻译方向选择
- 文本输入
- 翻译按钮
- 翻译结果展示
- 错误提示


调用链保持：

MainWindow

↓

TranslationFeature

↓

ModelService

↓

Runtime



---

# 禁止修改


以下模块禁止修改：


src/features/

src/services/

src/runtime/

src/integrations/

src/core/


除非为了 UI 类型适配必须调整。


禁止：

- 修改翻译逻辑
- 修改模型加载逻辑
- 修改快捷键逻辑
- 修改选中文字逻辑
- 修改 PopupWindow



---

# 不实现内容


本 Task 不包含：


- Settings 页面
- 历史记录
- PopupWindow 重构
- OCR
- 截图翻译
- 动画系统
- 多模型管理



---

# 验证要求


## 启动验证


执行：


python -m src.main



确认：

- 应用正常启动
- MainWindow 正常显示



---

## 功能验证


确认：


- 翻译方向切换正常
- 输入正常
- 翻译按钮正常
- 翻译结果正常显示



---

## 代码检查


必须通过：


ruff check .


black --check .


pip check


git diff --check



---

# Definition of Done


满足：

✅ MainWindow 按 Design 文档完成实现

✅ 公共 UI 组件建立

✅ Theme 系统正常使用

✅ Logo资源正常使用

✅ 原有翻译功能保持

✅ 未破坏 Runtime 和 Feature 架构

✅ 所有检查通过
