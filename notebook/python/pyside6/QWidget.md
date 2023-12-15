[TOC]

## Signal

customContextMenuRequested

windowIconChanged

windowIconTextChanged

windowTitleChanged

## Function

### Window functions

- `show()`: 显示窗口。
- `hide()`: 隐藏窗口。
- `raise_()`: 将窗口置于最前。
- `lower()`: 将窗口置于最后。
- `stackUnder(arg__1: PySide6.QtWidgets.QWidget)` 把窗口置于目标之下
- `close()`: 关闭窗口。

### Top-level windows

- `windowTitle() -> str`: 返回窗口的标题。
- `windowIcon() -> QIcon`: 返回窗口的图标。
- `isActiveWindow() -> bool`: 返回窗口是否是活动窗口。
- `activateWindow()`: 激活窗口，使其成为活动窗口。
- `showMinimized()`: 最小化窗口，将其图标化至任务栏。
- `showMaximized()`: 最大化窗口，使其充满整个屏幕。
- `showFullScreen()`: 全屏显示窗口。
- `showNormal()`: 恢复窗口原始大小和位置。

### Window contents

- `update()`:通知系统重绘小部件，触发 `paintEvent` 事件。
- `repaint()`: 类似于 `update()`，可传递矩形区域参数，指定需要重绘的区域。可以绕过比如"计时"等需要时间去处理的代码，但效率、效果不稳定，最好使用Qthread和update()
- `scroll(dx: int, dy: int)`: 接受两个整数参数，分别表示水平和垂直方向上的滚动距离。在小部件中实现滚动功能，通常与图形界面元素（如滚动条、文本框等）相关联。用途包括滚动视图、自动滚动、用户交互增强等。

### Geometry

- `pos() -> QPoint`: 返回小部件在其父部件坐标系中的位置。
- `x() -> int` 和 `y() -> int`: 分别返回小部件在其父部件坐标系的 x 和 y 坐标。
- `rect() -> QRect`: 返回小部件的内部矩形，不包括边框。
- `size() -> QSize`: 返回小部件的大小。
- `width() -> int` 和 `height() -> int`: 分别返回小部件的宽度和高度。
- `move(x: int, y: int)`: 移动小部件到一个指定的位置。
- `resize(width: int, height: int)`: 改变小部件的大小。
- `sizePolicy() -> QSizePolicy`: 返回小部件的尺寸策略。
- `sizeHint() -> QSize`: 返回小部件的建议尺寸。
- `minimumSizeHint() -> QSize`: 返回小部件的最小建议尺寸。
- `updateGeometry()`: 通知布局管理器此小部件的几何信息已更改。
- `layout() -> QLayout`: 返回小部件使用的布局管理器。
- `frameGeometry() -> QRect`: 返回小部件的外部矩形，包括边框和标题栏。
- `geometry() -> QRect`: 返回小部件的几何信息，包括位置和大小。
- `setGeometry(arg__1: PySide6.QtCore.QRect)`:可以设置内容边距
- `setGeometry(self, x: int, y: int, w: int, h: int)`
- `setContentsMargins(left: int, top: int, right: int, bottom: int)`:设置内容边距
- `setContentsMargins(margins: PySide6.QtCore.QMargins)`
- `childrenRect() -> QRect`: 返回包含所有子小部件的矩形。
- `childrenRegion() -> QRegion`: 返回包含所有子小部件的区域。
- `adjustSize()`: 调整小部件的大小以适应其内容。
- `mapFromGlobal(point: QPoint) -> QPoint` 和 `mapToGlobal(point: QPoint) -> QPoint`: 分别将全局坐标转换为小部件坐标，以及将小部件坐标转换为全局坐标。
- `mapFromParent(point: QPoint) -> QPoint` 和 `mapToParent(point: QPoint) -> QPoint`: 分别将父坐标转换为小部件坐标，以及将小部件坐标转换为父坐标。
- `maximumSize() -> QSize` 和 `minimumSize() -> QSize`: 分别返回小部件的最大和最小尺寸。
- `sizeIncrement() -> QSize`: 返回小部件的尺寸增量。
- `baseSize() -> QSize`: 返回小部件的基础尺寸，通常用于布局计算。
- `setFixedSize(size: QSize)` 或 `setFixedSize(width: int, height: int)`: 将小部件的大小固定在特定值。

### Mode

`isVisible() -> bool`: 返回小部件是否可见。
`setVisible(visible: bool)`
`isVisibleTo(parent: QWidget) -> bool`: 返回小部件相对于给定父小部件是否可见。
`isEnabled() -> bool`: 返回小部件是否启用。
`setEnabled(arg__1: bool)`
`isEnabledTo(parent: QWidget) -> bool`: 返回小部件相对于给定父小部件是否启用。
`isModal()`: 属性，表示小部件是否为模态。
`isWindow() -> bool`: 返回小部件是否为窗口。
`hasMouseTracking() -> bool`: 属性，表示是否启用鼠标跟踪。
`updatesEnabled() -> bool`: 属性，表示是否启用小部件的更新。
`visibleRegion() -> QRegion`: 返回小部件当前可见部分的区域。

### Look and feel

`style() -> QStyle`: 返回小部件的样式。
`setStyle(style: QStyle)`: 设置小部件的样式。
`styleSheet()`: 表示小部件的样式表。
`cursor()`: 表示小部件的光标。
`font()`: 表示小部件的字体。
`palette()`: 表示小部件的调色板。
`backgroundRole() -> QPalette.ColorRole`: 返回小部件的背景角色。
`setBackgroundRole(role: QPalette.ColorRole)`: 设置小部件的背景角色。
`fontInfo() -> QFontInfo`: 返回小部件字体的信息。
`fontMetrics() -> QFontMetrics`: 返回小部件字体的度量信息。

### Event handlers

- 基本事件处理
    `event(event: QEvent) -> bool`: 处理发生在小部件上的所有事件。

- 鼠标键盘事件
    `mousePressEvent(event: QMouseEvent)`: 处理鼠标按下事件。
    `mouseReleaseEvent(event: QMouseEvent)`: 处理鼠标释放事件。
    `mouseDoubleClickEvent(event: QMouseEvent)`: 处理鼠标双击事件。
    `mouseMoveEvent(event: QMouseEvent)`: 处理鼠标移动事件。
    `wheelEvent(event: QWheelEvent)`: 处理鼠标滚轮事件。
    `enterEvent(event: QEvent)`: 处理鼠标进入小部件的事件。
    `leaveEvent(event: QEvent)`: 处理鼠标离开小部件的事件。
    `keyPressEvent(event: QKeyEvent)`: 处理键盘按下事件。
    `keyReleaseEvent(event: QKeyEvent)`: 处理键盘释放事件。
    `dragEnterEvent(event: QDragEnterEvent)`: 处理拖动进入小部件的事件。
    `dragMoveEvent(event: QDragMoveEvent)`: 处理在小部件上拖动的事件。
    `dragLeaveEvent(event: QDragLeaveEvent)`: 处理拖动离开小部件的事件。
    `dropEvent(event: QDropEvent)`: 处理在小部件上放下拖动对象的事件。

- 焦点事件
    `focusInEvent(event: QFocusEvent)`: 处理获得焦点事件。
    `focusOutEvent(event: QFocusEvent)`: 处理失去焦点事件。

- 其他事件

    `paintEvent(event: QPaintEvent)`: 处理小部件的绘画事件。
    `moveEvent(event: QMoveEvent)`: 处理小部件移动的事件。
    `resizeEvent(event: QResizeEvent)`: 处理小部件大小改变的事件。
    `closeEvent(event: QCloseEvent)`: 处理小部件关闭的事件。

- 其他特殊事件
    `childEvent(event: QChildEvent)`: 处理子部件相关的事件。
    `showEvent(event: QShowEvent)`: 处理小部件显示的事件。
    `hideEvent(event: QHideEvent)`: 处理小部件隐藏的事件。
    `customEvent(event: QEvent)`: 处理自定义事件。
    `changeEvent(event: QEvent)`: 处理状态改变事件。

### System functions

`parentWidget() -> QWidget`: 返回小部件的父窗口。
`window() -> QWidget`: 返回小部件所属的顶级窗口。
`setParent(parent: QWidget)`: 设置小部件的父窗口。
`childAt(p: PySide6.QtCore.QPoint) -> PySide6.QtWidgets.QWidget`:获取处于指定坐标的子控件
`childAt(self, x: int, y: int) -> PySide6.QtWidgets`
`winId() -> int`: 返回小部件的窗口识别号。
`find(id: int) -> QWidget`: 根据窗口识别号查找小部件。
`metric(metric: QPaintDevice.PaintDeviceMetric) -> int`: 返回小部件的度量信息，如屏幕分辨率、字体大小等。

### Context menu

`contextMenuPolicy`: 属性，表示小部件的上下文菜单策略。
`customContextMenuRequested(position: QPoint)`: 当用户请求自定义上下文菜单时发出的信号。
`actions() -> List[QAction]`: 返回与小部件相关联的所有动作。

```python
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的上下文菜单策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # 添加一些动作
        self.actionOne = QAction("操作一", self)
        self.actionTwo = QAction("操作二", self)

        self.addAction(self.actionOne)
        self.addAction(self.actionTwo)
        

        # 连接动作的触发信号到槽函数
        self.actionOne.triggered.connect(lambda: self.on_action_triggered("操作一"))
        self.actionTwo.triggered.connect(lambda: self.on_action_triggered("操作二"))

    def on_context_menu(self, position):
        # 显示上下文菜单
        event = QContextMenuEvent(QContextMenuEvent.Mouse, position)
        context_menu = QMenu(self)
        context_menu.addAction(self.actionOne)
        context_menu.addAction(self.actionTwo)
        context_menu.exec(event.globalPos())

    def on_action_triggered(self, action_name):
        QMessageBox.information(self, "操作触发", f"你选择了: {action_name}")

app = QApplication(sys.argv)
window = CustomMainWindow()
window.resize(400, 300)  # 设置窗口初始大小
window.show()
sys.exit(app.exec())

```

### Interactive help

setToolTip()
setWhatsThis()

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QWhatsThis

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 创建一个按钮并设置工具提示
        btn1 = QPushButton("按钮1", self)
        btn1.setToolTip("这是 <b>按钮1</b> 的工具提示")
        layout.addWidget(btn1)

        # 创建另一个按钮并设置“这是什么”信息
        btn2 = QPushButton("按钮2", self)
        btn2.setWhatsThis("这是按钮2的 'What's This' 信息")
        layout.addWidget(btn2)

        # 创建一个按钮用于激活 What's This 模式
        whatsThisButton = QPushButton("显示 What's This 信息", self)
        whatsThisButton.clicked.connect(self.showWhatsThis)
        layout.addWidget(whatsThisButton)

        self.setLayout(layout)
        self.setWindowTitle("工具提示和 What's This 示例")

    def showWhatsThis(self):
        QWhatsThis.enterWhatsThisMode()

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())

```

### Cursor

`QWidget.setCursor(QCursor)`  设置光标形状
`QWidget.unsetCursor()`  取消设置光标形状
`QWidget.cursor() -> QCursor`  获取光标形状

```python
pixmap = QtGui.QPixmap("img.png").scaled(52, 52)
my_cursor = QtGui.QCursor(pixmap, 26, 26)  # 以图片像素点位置26,26为热点（光标实际所在位置坐标）
self.setCursor(my_cursor)
# 设置label中的光标为Qt内置的其他光标
self.label.setCursor(Qt.ForbiddenCursor)
# self.label.setCursor(Qt.OpenHandCursor)
```
## Signal

customContextMenuRequested

windowIconChanged

windowIconTextChanged

windowTitleChanged

## Function

### Window functions

- `show()`: 显示窗口。

- `hide()`: 隐藏窗口。

- `raise()`: 将窗口置于最前。

- `lower()`: 将窗口置于最后。

- `close()`: 关闭窗口。

### Top-level windows

- `windowTitle() -> str`: 返回窗口的标题。

- `windowIcon() -> QIcon`: 返回窗口的图标。

- `isActiveWindow() -> bool`: 返回窗口是否是活动窗口。

- `activateWindow()`: 激活窗口，使其成为活动窗口。

- `showMinimized()`: 最小化窗口，将其图标化至任务栏。

- `showMaximized()`: 最大化窗口，使其充满整个屏幕。

- `showFullScreen()`: 全屏显示窗口。

- `showNormal()`: 恢复窗口原始大小和位置。

>activateWindow可以用在临时新建了一个窗口，并把它激活的功能上
>
### Window contents

- `update()`:通知系统重绘小部件，触发 `paintEvent` 事件。
- `repaint()`: 类似于 `update()`，可传递矩形区域参数，指定需要重绘的区域。可以绕过比如"计时"等需要时间去处理的代码，但效率、效果不稳定，最好使用Qthread和update()
- `scroll(dx: int, dy: int)`: 接受两个整数参数，分别表示水平和垂直方向上的滚动距离。在小部件中实现滚动功能，通常与图形界面元素（如滚动条、文本框等）相关联。用途包括滚动视图、自动滚动、用户交互增强等。

### Geometry

- `pos() -> QPoint`: 返回小部件在其父部件坐标系中的位置。
- `x() -> int` 和 `y() -> int`: 分别返回小部件的 x 和 y 坐标。
- `rect() -> QRect`: 返回小部件的内部矩形，不包括边框。
- `size() -> QSize`: 返回小部件的大小。
- `width() -> int` 和 `height() -> int`: 分别返回小部件的宽度和高度。
- `move(x: int, y: int)`: 移动小部件到一个指定的位置。
- `resize(width: int, height: int)`: 改变小部件的大小。
- `sizePolicy() -> QSizePolicy`: 返回小部件的尺寸策略。
- `sizeHint() -> QSize`: 返回小部件的建议尺寸。
- `minimumSizeHint() -> QSize`: 返回小部件的最小建议尺寸。
- `updateGeometry()`: 通知布局管理器此小部件的几何信息已更改。
- `layout() -> QLayout`: 返回小部件使用的布局管理器。
- `frameGeometry() -> QRect`: 返回小部件的外部矩形，包括边框和标题栏。
- `geometry() -> QRect`: 返回小部件的几何信息，包括位置和大小。
- `childrenRect() -> QRect`: 返回包含所有子小部件的矩形。
- `childrenRegion() -> QRegion`: 返回包含所有子小部件的区域。
- `adjustSize()`: 调整小部件的大小以适应其内容。
- `mapFromGlobal(point: QPoint) -> QPoint` 和 `mapToGlobal(point: QPoint) -> QPoint`: 分别将全局坐标转换为小部件坐标，以及将小部件坐标转换为全局坐标。
- `mapFromParent(point: QPoint) -> QPoint` 和 `mapToParent(point: QPoint) -> QPoint`: 分别将父坐标转换为小部件坐标，以及将小部件坐标转换为父坐标。
- `maximumSize() -> QSize` 和 `minimumSize() -> QSize`: 分别返回小部件的最大和最小尺寸。
- `sizeIncrement() -> QSize`: 返回小部件的尺寸增量。
- `baseSize() -> QSize`: 返回小部件的基础尺寸，通常用于布局计算。
- `setFixedSize(size: QSize)` 或 `setFixedSize(width: int, height: int)`: 将小部件的大小固定在特定值。


