from PySide6.QtCore import QAbstractListModel, QAbstractItemModel, QModelIndex, Qt
from PySide6 import QtGui
import mupy as mu
import uipy as ui


class ListModel(QAbstractListModel):
    """列表模型。

    数据格式可以按：
    1.简单
    ['1','2','3',...]
    2.对象
    [{text:'',icon:''},...] 格式，其中可按需求增补 id/value/checked 字段
    3.随意
    需要给出 textCallback 和 iconCallback 来返回具体的 text/icon 数据，如没有 icon，返回 ''。

    """
    items = []

    defaultIcon = ''
    textCallback = None
    iconCallback = None

    def __init__(this, items):
        super(ListModel, this).__init__()
        this.items = items

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(this, index, role):
        row = index.row()
        return ui.handleModelData(this.items[row], role, None, this.textCallback, this.iconCallback, this.defaultIcon)

    def setData(this, index, value, role):
        if role == Qt.CheckStateRole:
            item = this.items[index.row()]
            chk = mu.getValue(item, 'checked')
            mu.setValue(item, not chk)

        return True

    def rowCount(this, parent):
        return len(this.items)

    def add(this, item):
        this.items.append(item)
        this.layoutChanged.emit()

    def insert(this, index, item):
        this.items.insert(index.row(), item)
        this.layoutChanged.emit()

    def remove(this, item):
        this.items.remove(item)
        this.layoutChanged.emit()

    def update(this, index, newItem):
        this.items[index.row()] = newItem
        this.dataChanged.emit(index, index)
