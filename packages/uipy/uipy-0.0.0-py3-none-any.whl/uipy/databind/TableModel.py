from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6 import QtGui
import mupy as mu
import uipy as ui


class TableModel(QAbstractTableModel):

    items = []
    hHeaderItems = []
    vHeaderItems = []

    def __init__(this, items, hHeaderItems=[], vHeaderItems=[]):
        super(TableModel, this).__init__()
        this.items = items
        this.hHeaderItems = hHeaderItems
        this.vHeaderItems = vHeaderItems

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(this, parent):
        return len(this.items)

    def columnCount(this, parent):
        return len(this.hHeaderItems)

    def headerData(this, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                len1 = len(this.hHeaderItems)
                if section > len1 - 1:
                    return None
                return ui.handleModelData(this.hHeaderItems[section], role)
            else:
                len1 = len(this.vHeaderItems)
                if section > len1 - 1:
                    return None
                return ui.handleModelData(this.vHeaderItems[section], role)

    def data(this, index, role):
        row, column = index.row(), index.column()
        item = this.items[row][column]
        return ui.handleModelData(item, role)
