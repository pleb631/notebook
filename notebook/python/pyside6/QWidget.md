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


