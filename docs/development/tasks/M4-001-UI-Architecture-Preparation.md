# M4-001 UI Architecture Preparation


## Task目标

为 LinguaFlow UI 产品化重构建立基础架构。

本 Task 只负责 UI 基础设施准备。

禁止实现具体 UI 页面。


---

# 修改文件


## 修改

src/app/application.py


---

# 新增目录


src/ui/components/

src/ui/theme/

src/ui/styles/

src/ui/resources/

src/ui/pages/


---

# 新增文件


src/ui/components/__init__.py


src/ui/theme/__init__.py

src/ui/theme/theme.py


src/ui/styles/__init__.py

src/ui/styles/stylesheet.py


src/ui/resources/__init__.py

src/ui/resources/assets.py


src/ui/pages/__init__.py



---

# 实现要求


## 1. Theme系统


新增：

src/ui/theme/theme.py


统一管理UI设计变量。


必须包含：

颜色：

- background
- surface
- primary
- text
- secondary_text
- border
- success
- error


圆角：

small

medium

large


间距：

xs

sm

md

lg

xl



要求：

后续UI禁止硬编码颜色。


---

# 2. Stylesheet入口


新增：

src/ui/styles/stylesheet.py


提供：


build_stylesheet()


返回Qt StyleSheet字符串。


当前只建立入口。


不要求完成全部视觉样式。


---

# 3. Logo资源管理


新增：

src/ui/resources/assets.py


负责统一管理assets目录。


已有资源：

assets/


包含：

logo16.png

logo32.png

logo512.png



提供：

get_logo(size)



支持：

16

32

512



禁止重新生成Logo。


---

# 4. Application接入


修改：

src/app/application.py


Application启动流程：


创建 QApplication


↓

加载全局stylesheet


↓

创建AppContext


↓

创建MainWindow



要求：

不改变现有业务流程。


---

# 5. 目录规范


最终结构：


src/ui/

├── components/

├── theme/

├── styles/

├── resources/

├── pages/

├── workers/

├── main_window.py

└── popup_window.py



---

# 明确禁止


本Task禁止：


- 修改MainWindow布局

- 修改PopupWindow样式

- 新增UI组件

- 新增Settings页面

- 修改翻译功能

- 修改模型逻辑

- 修改快捷键逻辑


---

# 验证要求


必须通过：


python -m src.main


ruff check .


black --check .


pip check


git diff --check



---

# Definition of Done


满足：

✅ UI基础目录建立

✅ Theme入口完成

✅ Stylesheet入口完成

✅ Logo资源统一管理

✅ Application加载UI基础设施

✅ 原有翻译功能不受影响
