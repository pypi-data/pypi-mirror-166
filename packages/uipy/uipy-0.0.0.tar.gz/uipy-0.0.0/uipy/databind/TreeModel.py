from PySide6.QtCore import QAbstractListModel, QAbstractItemModel, QModelIndex, Qt
from PySide6 import QtGui
import mupy as mu
import uipy as ui


class TreeModel(QAbstractItemModel):

    items = []
    hHeaderItems = []
    vHeaderItems = []

    def _handleParentData(this, item, parent, depth):
        item['_parent_'] = parent

    def __init__(this, items, hHeaderItems=[], vHeaderItems=[]):
        super(TreeModel, this).__init__()
        this.items = items
        this.hHeaderItems = hHeaderItems
        this.vHeaderItems = vHeaderItems

        # 增补每个元素的 _parent_ 属性，表示对应父级
        mu.traverseList(this.items, this._handleParentData)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # 获取节点数据
    def data(this, index, role):
        # internalPointer 实际上就是当前节点原始数据（this.items 里面的一个或 children 里面的一个）
        return ui.handleModelData(index.internalPointer(), role, index.column())

    def headerData(this, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ui.handleModelData(this.hHeaderItems[section], role)
            else:
                return ui.handleModelData(this.vHeaderItems[section], role)

    # 通过子节点索引获取父节点索引
    def parent(this, child):
        if not child.isValid():
            return QModelIndex()

        p = child.internalPointer()['_parent_']
        if p is None:
            return QModelIndex()

        i = -1
        pp = p['_parent_']
        # 如果没有上级，就是 items 里面
        if pp is None:
            for j in range(len(this.items)):
                item = this.items[j]
                if id(item) == id(p):
                    i = j
                    break
        # 有上级，就看自己在上级的哪里
        else:
            for j in range(len(pp['children'])):
                item = pp['children'][j]
                if id(item) == id(p):
                    i = j
                    break

        return this.createIndex(i, 0, p)

    # 获取父节点下子节点的行数
    def rowCount(this, parent):
        # 如果不合法（row=-1,column=-1），则是请求根节点
        if not parent.isValid():
            return len(this.items)
        else:
            chs = mu.getValue(parent.internalPointer(), 'children')
            if chs is None:
                return 0
            else:
                return len(chs)

    # 获取父节点下子节点列数
    def columnCount(this, parent):
        return len(this.hHeaderItems)

    # 构造父节点下子节点的索引
    def index(this, row, column, parent):

        if not this.hasIndex(row, column, parent):
            return QModelIndex()

        child = None
        if not parent.isValid():
            child = this.items[row]
        else:
            child = parent.internalPointer()['children'][row]

        return this.createIndex(row, column, child)
