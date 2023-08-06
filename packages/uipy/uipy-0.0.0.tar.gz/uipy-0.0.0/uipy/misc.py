from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QListView, QTreeView, QTableView, QButtonGroup, QComboBox, QRadioButton, QCheckBox, QWidget, QLayout
from PySide6.QtGui import QScreen

import mupy as mu
import uipy as ui


def getMW():
    """获取主窗口

    Returns:
        QMainWindow: 主窗口，没获取到返回 None
    """

    for w in QApplication.topLevelWidgets():
        if w.inherits('QMainWindow'):
            return w

    return None


def eachChild(callback, parent=None):
    """遍历孩子控件

    Args:
        callback (function): 回调，原型为 callback(child)，终止回调请返回 False
        parent (QWidget, optional): 父亲. Defaults to None.
    """
    if parent is None:
        parent = getMW()

    for child in parent.children():

        if (not isinstance(child, QWidget)) and (not isinstance(child, QButtonGroup)):
            continue

        r = callback(child)
        if r is False:
            break

        eachChild(callback, child)


def eachChildLayout(callback, parentWidget=None):

    if parentWidget is None:
        parentWidget = getMW()

    # QWidget 的 children() 是包含 QLayout 和 QWidget 的，故可以从组件角度深度遍历，
    # 但 QLayout 的 children() 只包含 QLayout。
    for child in parentWidget.children():

        if isinstance(child, QLayout):
            r = callback(child)
            if r is False:
                break

            eachChildLayout(callback, child)

        elif isinstance(child, QWidget):
            eachChildLayout(callback, child)


def findLayoutByWidget(widget):

    layout = None

    def callback(child):
        nonlocal layout

        for i in range(child.count()):
            w = child.itemAt(i).widget()
            if w == widget:
                layout = child
                return False

    eachChildLayout(callback)

    return layout


def F(name):
    """获取子组件

    Args:
        name (str|QWidget): 名称|类型

    Returns:
        QWidget: 子控件，没获取到返回 None
    """

    r = None

    def callback(child):
        nonlocal r

        if isinstance(child, str):
            if child.name == name:
                r = child
                return False
        else:
            if isinstance(child, name):
                r = child
                return False

    eachChild(callback)

    return r


def addButtonsToGroup(items, group, parent, type, clear=True):
    """添加按钮到按钮组

    Args:
        items (ui.ListModel): 项集合
        group (QButtonGroup): 组
        parent (QWidget): 父亲
        type (str): 类型，radio、checkbox
        clear (bool, optional): 是否清除已有按钮. Defaults to True.
    """
    layout = None
    # 先清除所有
    for btn in group.buttons():
        layout = findLayoutByWidget(btn)

        if clear is False:
            break

        group.removeButton(btn)
        layout.removeWidget(btn)
        btn.setParent(None)
        btn.deleteLater()

    # 再加
    for item in items:
        btn2 = None
        if type == 'radio':
            btn2 = QRadioButton(item['text'], parent)
        elif type == 'checkbox':
            btn2 = QCheckBox(item['text'], parent)

        group.addButton(btn2, item['id'])
        layout.addWidget(btn2)


def checkButtons(group, ids, type='selectId'):

    for i, btn in enumerate(group.buttons()):
        btn.setChecked(False)
        id = group.id(btn)

        if not mu.islist(ids):
            ids = [ids]

        if type == 'selectId' and ids.count(id) == 1:
            btn.setChecked(True)
        if type == 'selectIndex' and ids.count(i) == 1:
            btn.setChecked(True)


def center2Screen(widget):
    ssize = QScreen.availableGeometry(QApplication.primaryScreen())
    x = (ssize.width() - widget.width()) / 2
    y = (ssize.height() - widget.height()) / 2
    widget.move(x, y)


def center2Parent(widget):
    ssize = widget.parent().geometry()
    x = (ssize.width() - widget.width()) / 2
    y = (ssize.height() - widget.height()) / 2
    widget.move(x, y)


def center2QMW(widget):
    ssize = getMW().geometry()
    x = (ssize.width() - widget.width()) / 2
    y = (ssize.height() - widget.height()) / 2
    widget.move(x, y)
