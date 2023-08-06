# uipy 编程指南

## 1. 概述

uipy 是基于 pyside 6 的二次封装，包含如下特性：

- MVVM
  
  简单 mvvm 模型，开发更方便。

- .ui 生成
  
  依赖 webmix，用 js 语言撰写原生 .ui 文件

- DOM 操作
  
  模仿 jquery 对组件进行操作

- EventDispatcher
  
  模仿 jquery 事件机制，将 pyside 的 Event、Action、Signal+Slot 改为 jquery 事件模式，写起来更顺手

- widget
  
  包含一套具有 databind 属性的控件。
  
  包含一系列新的组件。

依靠这些特性，编程的感觉就与 javascript 开发类似了。

## 2. 第一步

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
# 本文示例中 ui 均表示 uipy 模块
import uipy as ui

if __name__ == "__main__":

    # 全局只调用一次，推荐在主.py文件中调用
    ui.init()

    app = QApplication(sys.argv)
    window = QMainWindow()
    # 设定主窗口，方便后续使用，也可以调用 ui.getMW() 来获得
    ui.QMW = window
    window.show()

    sys.exit(app.exec())
```

## 3. 功能



### 3.1 派发器

Dispatcher，融合 Action、Event、Signal & Slot，并提供类似 jquery 的使用方法。

- uuid
  唯一编号

- on(signal,slot)
  侦听信号

- off(signal,slot)
  断开侦听

- fire(signal,*args)
  触发信号

简单示例：

```python
# 因 python 没有 js 那种匿名函数，只能这样写
def click1():
    pass

label1.on(label1.clicked,click1)

# 自定义信号
label1.fire('signal1')
label1.fire('signal1','hello')
```

### 3.2 数据绑定

数据双向绑定器。

ViewModel 作为视图模型基类。

Binder 统管 DataBinder、Observable、ViewModel 三者，并且可以通过 ui.BINDER 全局访问到。

DataBinder 与组件绑定，为组件连通 Observable 提供桥梁，如：

```python
name=ui.Observable('jerry')
label1.databind={'str',name}
```

数据流只有两个方向，一是从值变更触发组件变更，如：

```python
name.set('jerry1979')
```

将会导致 label1 显示的文本改变。

二是从组件本身变更触发值的改变，如文本框里面的值被用户修改，会同时改变绑定的 Observable 里面的值。

数据流的两个方向的改变均由 Binder 总控。

除了数据流以外，还有信号流，信号流绑定的不再是 Observable 对象，而是一个函数，如：

```python
def click1():
    pass

button1.databind={'click',click1}
```

#### 3.2.1 绑定类型

- 值类型

  可以为：str/int/float/bool/color/date/datetime/time，

  绑定的是一个字符串、整数、浮点数、布尔、颜色、日期、日期时间、时间。

- 行为
  
  可以为：visible/enable，表明可见和可用。

- 信号

  可以为：click/dbclick/select，表明点击、双击和列表类（列表、树形、表格、单选钮组、复选框组、下拉框）选择信号。双击仅用于 list/tree/table。

- 集合类

  可以为：list/tree/table/combobox/radioGroup/checkboxGroup，表明为列表、树形、表格、下拉框、单选钮组、复选框组提供的数据源（model）。

- 选择类
  
  可以为：selectItem/selectIndex/selectValue/selectText/selectId，表明当前选中的项/索引/值/文本。
  要注意，list/tree/talbe 的 selectIndex 为 QModelIndex 类型（可以通过 QAbstractItemModel::createIndex 来创建），而 combobox/radioGroup/checkboxGroup 的 selectIndex 为选择的索引（从0开始）。

#### 3.2.2 Observable/ObservableArray

用于绑定。

共有方法：

- get/set
  
  取值，赋值

ObservableArray 独有方法：

- add/insert/remove/update

  添加、插入、移除、更新。

举例：
```python

name=ui.Observable('jerry')
print(name.get())
name.set('jerry1979')
print(name.get())

shapes = ui.ObservableArray(ui.ListModel([{
    'text': '三角形',
    'icon': './imgs/triangle.png'
}, {
    'text': '圆形',
    'icon': './imgs/circle.png',
    'age': 12
}, {
    'text': '矩形',
    'icon': './imgs/rect.png'
}]))
shapes.add({
    'text': '矩形2',
    'icon': './imgs/rect.png'
})


```

## 4. 其他API

### QMW

本应用主窗口。

```python
print(ui.QMW.name)
```

### F

依据名称或类型找控件。

```python
label1=ui.F('label1')
label1=ui.F(QLabel)
```

### eachChild

遍历孩子控件。

### eachChildLayout

遍历孩子布局。

### findLayoutByWidget

通过组件找到自己的或所在的布局。

### addButtonsToGroup

增加按钮到按钮组。

### checkButtons

选择按钮组中的按钮。

### center2Screen/center2Parent/center2QMW

居中对齐，相对于屏幕、父亲、主窗口。


## 5. 扩展组件

### ColorButton

点击可以弹出颜色选择框的按钮。


## 6. 示例

详见 examples 下面。

## 7. 其他

### 全局异常

对于全局未捕获异常，自动抓取，并弹出消息框。

如果未弹出，程序退出了，可以查看应用程序下的 UncaughtHook.txt 文件。

## 8. 依赖

- pyside 6

- mupy
  
  一套 python 的各类工具集

- webmix
  
  一套生成 .ui 文件的界面撰写语言。依赖于 pyside6 designer.exe 和 uic.exe。