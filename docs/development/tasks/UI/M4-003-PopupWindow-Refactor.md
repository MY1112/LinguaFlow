# M4-003 PopupWindow Refactor


## Task ID

M4-003


## Task Name

PopupWindow 产品化重构



# 1. Task目标


根据 LinguaFlow PopupWindow 设计规范，对现有 PopupWindow 进行产品化重构。


目标：

提升快捷翻译场景下的交互体验。


核心使用场景：


用户选中文字


↓

Alt + Q


↓

获取选中文本


↓

执行翻译


↓

PopupWindow 展示结果



本 Task 只负责 PopupWindow UI 与交互体验优化。


---

# 2. Design依据


必须遵循以下 Design 文档：


docs/design/20-Design-System.md


docs/design/21-Brand-Identity.md


docs/design/23-PopupWindow-Spec.md


docs/design/25-Component-Spec.md



Design 文档为唯一视觉规范来源。


如果 Task 描述与 Design 文档冲突：

以 Design 文档为准。


---

# 3. 修改范围


## 修改文件


src/ui/popup_window.py



---

## 新增文件


如现有组件无法满足 Design 要求：

可在以下目录新增组件：


src/ui/components/


新增组件必须符合：

docs/design/25-Component-Spec.md



---

# 4. 功能保持


PopupWindow 必须保持现有公开接口。


例如：


show_result(text)


现有调用方无需修改。



---

# 5. 快捷翻译链路保持


必须保持当前调用链：


HotkeyAdapter


↓

SelectionAdapter


↓

TranslationFeature


↓

PopupWindow



禁止改变：

- 快捷键逻辑
- 选中文字逻辑
- 翻译逻辑



---

# 6. UI实现要求


根据：

docs/design/23-PopupWindow-Spec.md


完成：


- Popup视觉升级
- 内容展示优化
- 状态展示优化
- 交互体验优化


具体：

- 尺寸
- 布局
- 样式
- 颜色
- 字体

全部遵循 Design 文档。



---

# 7. Theme要求


PopupWindow 必须使用：


src/ui/theme/theme.py


src/ui/styles/stylesheet.py



禁止：

- 硬编码颜色
- 重复定义设计变量
- 绕过Theme系统



---

# 8. 组件复用要求


优先复用已有公共组件：


src/ui/components/


避免：

- 重复实现按钮
- 重复实现卡片
- 重复实现状态展示



---

# 9. 不修改范围


禁止修改：


src/features/


src/services/


src/runtime/


src/integrations/


src/core/



除非为 UI 类型适配必须修改。


禁止：

- 修改 TranslationFeature
- 修改 ModelService
- 修改 RuntimeManager
- 修改 HotkeyAdapter
- 修改 SelectionAdapter



---

# 10. 不实现内容


本 Task 不包含：


- OCR
- 截图翻译
- 历史记录
- 收藏功能
- 设置页面
- 多模型管理
- Prompt编辑
- 翻译模型优化



---

# 11. 验证要求


## 应用启动


执行：


python -m src.main



确认：

- 应用正常启动
- Popup相关功能无异常



---

## Popup验证


确认：


- Popup可以正常显示
- Popup可以正常隐藏
- 自动隐藏逻辑正常
- 不进入任务栏
- 不影响主窗口操作



---

## 快捷翻译验证


验证：


选中文字


↓

Alt + Q


↓

Popup展示翻译结果



---

## 代码检查


必须通过：


ruff check .


black --check src tests


pip check


git diff --check



---

# 12. Definition of Done


满足：


✅ PopupWindow按照Design规范完成重构


✅ 快捷翻译链路保持正常


✅ 公共组件体系正常使用


✅ Theme系统正常接入


✅ 未修改业务层架构


✅ 所有检查通过
