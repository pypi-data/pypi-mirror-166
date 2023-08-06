import uipy as ui
import mupy as mu
from PySide6.QtCore import QDate, QDateTime, QTime, Qt
from PySide6 import QtGui


def fromObj(obj):
    keys = mu.getProperties(obj)
    r = {}
    for key in keys:
        val = mu.getValue(obj, key)
        if mu.isvalue(val) or mu.isbool(val) or isinstance(val, QDate) or isinstance(val, QTime) or isinstance(val, QDateTime):
            r[key] = ui.Observable(val)
        elif mu.islist(val):
            r[key] = ui.ObservableArray(val)
        elif mu.isdict(val) or mu.isobject(val):
            r[key] = fromObj(val)

    return mu.dict2Object(r)


def toObj(obj):
    pass


def isObservable(val):

    if hasattr(val, 'type') and val.type == 'observable':
        return True
    return False


def isObservableArray(val):

    if hasattr(val, 'type') and val.type == 'observableArray':
        return True
    return False


def appendItem(oarr, obj):

    fn = oarr.__name__
    arr = oarr()
    arr.append(obj)
    ui.BINDER['datas'][fn] = arr


def removeItem(oarr, obj):
    fn = oarr.__name__
    arr = oarr()
    arr.remove(obj)
    ui.BINDER['datas'][fn] = arr
    ui.BINDER.fire('change', oarr, obj)


def removeItems(oarr, idxs):
    fn = oarr.__name__
    arr = oarr()
    mu.removeItems(arr, idxs)
    ui.BINDER['datas'][fn] = arr


def handleModelData(item, role, column=None, textCallback=None, iconCallback=None, defaultIcon=None):

    if role == Qt.DisplayRole:
        text = ''

        if textCallback is not None:
            text = textCallback(item, column)
        else:
            if mu.isvalue(item):
                text = str(item)
            else:
                text = mu.getValue(item, 'text')
                if mu.islist(text) and column is not None:
                    text = text[column]

        return text

    if role == Qt.DecorationRole:
        icon = ''

        if iconCallback is not None:
            icon = iconCallback(item, column)
        else:
            if mu.isvalue(item):
                icon = ''
            else:
                icon = mu.getValue(item, 'icon')
                if mu.islist(icon) and column is not None:
                    icon = icon[column]

        if mu.isN(icon):
            if mu.isNN(defaultIcon):
                return QtGui.QImage(defaultIcon)
        else:
            return QtGui.QImage(icon)

    if role == Qt.CheckStateRole:

        chk = mu.getValue(item, 'checked')
        if mu.islist(chk) and column is not None:
            chk = chk[column]

        if chk is not None:
            return Qt.Checked if chk == True else Qt.Unchecked

    if role == Qt.UserRole:
        return item

    return None
