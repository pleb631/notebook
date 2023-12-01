## Signal

destroyed

objectNameChanged

## Function

### **事件处理**

* `event(self, event)`: 事件处理函数，用于处理所有发送到该对象的事件。
* `installEventFilter(self, filterObj)`: 安装事件过滤器到该对象。
* `removeEventFilter(self, filterObj)`: 移除之前安装的事件过滤器。

```python
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PySide6.QtCore import QObject, QEvent
class EventFilter(QObject):
    def eventFilter(self, obj, event):
        # 当按钮被点击时
        if event.type() == QEvent.MouseButtonPress:
            print("Button clicked - event filter")
            return True
        return False
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建按钮
        self.button = QPushButton("Click me", self)
        self.button.setGeometry(50,50, 100, 50)
        self.button.pressed.connect(lambda:print("!"))
        self.button1 = QPushButton("change mode", self)
        self.button1.setGeometry(200,50, 100, 50)
        self.button1.pressed.connect(self.change)
        # 创建事件过滤器并安装
        self.filter = EventFilter()
        self.button.installEventFilter(self.filter)
        self.installed=True
        self.label = QLabel("Event label", self)
        self.label.setGeometry(100, 150, 200, 30)
    def event(self, event):
        # 处理窗口本身的事件
        if event.type() == QEvent.MouseButtonPress:
            self.label.setText("Window clicked")
            return True
        return super().event(event)
    def change(self,):
        if self.installed:
            self.button.removeEventFilter(self.filter)
            self.installed=False
        else:
            self.button.installEventFilter(self.filter)
            self.installed=True
if __name__=='__main__':
    app = QApplication(sys.argv)
     window = MyWindow()
     window.show()
     sys.exit(app.exec())
```

### **对象属性和元对象系统**

* `setProperty(self, name, value)`: 设置对象的属性。
* `property(self, name)`: 获取对象的属性。
* `objectName(self)`: 获取对象的名称。
* `setObjectName(self, name)`: 设置对象的名称。
* `metaObject(self)`: 获取对象的元对象信息，包含信号、槽、属性等信息。

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口的名称
        self.setObjectName("MainWindow")
        # 创建一个按钮，并设置一些属性
        self.button = QPushButton("Click me", self)
        self.button.setObjectName("MyButton")
        self.button.setProperty("type", "pushbutton")
        self.button.setGeometry(50, 50, 100, 30)
        # 创建一个标签来显示信息
        self.label = QLabel("", self)
        self.label.setGeometry(50, 100, 300, 50)
        button_type = self.button.property("type")
        button_name = self.button.objectName()
        meta_obj = self.button.metaObject().className()
        self.label.setText(f"Button Name: {button_name}\n"
                           f"Button Type: {button_type}\n"
                           f"Meta Object Class: {meta_obj}")
        # 连接按钮的信号
        self.button.clicked.connect(self.on_button_clicked)
    def on_button_clicked(self):
        # 获取按钮的属性并显示在标签上
        self.label.setObjectName('test')
        self.label.setProperty('name', 'test1')
        print(self.label.property('name'),self.label.objectName())
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
```

### **对象的父子关系**

* `parent(self)`: 返回对象的父对象。
* `setParent(self, parent)`: 设置对象的父对象。
* `findChild(self, type, name)`: 查找满足条件的第一个子对象。
* `findChildren(self, type, name)`: 查找所有符合条件的子对象。
* `children(self)`: 返回对象的直接子对象列表。
* `deleteLater(self)`: 将对象标记为删除，当控制权返回到事件循环时，对象将被删除。
* `inherits(self, className)`: 检查对象是否继承自指定的类。
* `isWidgetType(self)`: 判断该对象是否是一个小部件。
* `isWindowType(self)`: 判断该对象是否是一个窗口。

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import pprint

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")

        # 创建一个按钮，并设置一些属性
        self.button = QPushButton("Click me")
        self.button.setParent(self)
  
        self.button.objectNameChanged.connect(lambda:print("name chageed"))
        self.button.setObjectName("MyButton")
        self.button.setProperty("type", "pushbutton")
        self.button.setGeometry(50, 50, 100, 30)
        print(
            self.button.isWidgetType(),
            self.button.isWindowType(),
            self.isWindowType(),
        )
        pprint.pprint([self.button.parent(),
              self.findChild(QPushButton),
              self.children()])

        # 连接按钮的信号
        self.button.clicked.connect(self.on_button_clicked)
  
        self.button.destroyed.connect(lambda:print("delete!!"))

    def on_button_clicked(self):
        self.button.deleteLater()



app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())

```

### **信号的连接和阻隔、计时器**

`blockSignals(self, bool)`:临时阻止/允许对象发出信号。返回之前的阻止状态
`connectNotify(self, QMetaMethod)`:当一个新的信号连接到对象的槽时调用
`timerEvent(self, QTimerEvent)`:处理计时器事件
`startTimer(self, int interval, Qt.TimerType timerType=Qt.PreciseTimer)`:启动一个计时器
`signalsBlocked(self)`:检查对象是否阻止了信号

```python
import sys
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class CustomObject(QObject):
    customSignal = Signal()

    def __init__(self):
        super().__init__()
        self.timer_id = self.startTimer(2000)  # 启动计时器，每两秒触发一次

    def timerEvent(self, event):
        print("trigger1")
        if event.timerId() == self.timer_id:
            self.customSignal.emit()

    def connectNotify(self, signal):
        print(f"Signal '{signal.name()}' connected")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.obj = CustomObject()
  
        self.button = QPushButton("Block/dis Signal", self)
        self.button.clicked.connect(self.emit_signal)
        self.button.move(50, 20)
  
        self.button = QPushButton("connect/dis", self)
        self.button.clicked.connect(self.reverse_signal)
        self.button.move(50, 50)
  
        self.obj.customSignal.connect(self.test)
        self.connect=True
  
    def emit_signal(self):
  
        block_status = not self.obj.signalsBlocked()
        self.obj.blockSignals(block_status)
        print(f"Signals blocked: {self.obj.signalsBlocked()}")

    def reverse_signal(self):   
        if self.connect:
            self.obj.customSignal.disconnect(self.test)
        else:
            self.obj.customSignal.connect(self.test)
  
        self.connect = not self.connect
  
    def test(self):
        print("trigger2")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())

```

### **Qthread**

`moveToThread(self, thread: PySide6.QtCore.QThread)`: 把对象从一个线程移动到另一个线程
`thread（self）`返回线程的地址

```python
import sys
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import time

class Worker(QObject):
    finished = Signal()
    progress = Signal(int)

    def run(self):
        for i in range(0, 5):
            time.sleep(0.5)  # 模拟长时间运行的任务
            self.progress.emit(i + 1)
        self.finished.emit()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.label = QLabel("Task not started", self)
        self.layout.addWidget(self.label)

        self.button = QPushButton("Start Task", self)
        self.button.clicked.connect(self.startTask)
        self.layout.addWidget(self.button)

        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        print(self.worker.thread(),self.thread)

        self.worker.finished.connect(self.thread.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        #self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)

    def startTask(self):
        self.worker.finished.connect(self.taskFinished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        self.button.setEnabled(False)

    @Slot()
    def reportProgress(self, n):
        self.label.setText(f"Progress: {n}")

    @Slot()
    def taskFinished(self):
        self.label.setText("Task finished!")
        self.button.setEnabled(True)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())

```
