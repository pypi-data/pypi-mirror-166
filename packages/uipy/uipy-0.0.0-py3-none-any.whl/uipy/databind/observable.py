import uipy as ui
import uuid as uid


class _Observable(ui.Dispatcher):

    uuid = ''
    type = '_observable'
    value = None

    # 对应的 QModelIndex，用于修改本对象回头更新对应的 list/table/tree 等集合类组件
    index = None

    def __init__(this, val):

        super(_Observable, this).__init__()
        this.value = val
        ui.BINDER.observables.append(this)

    def get(this):
        return this.value

    def set(this, val, idx=None):
        this.value = val
        this.index = idx
        this.fire('change', this)
        ui.BINDER.fire('changeFromObservable', this)


class Observable(_Observable):

    def __init__(this, val):
        super(Observable, this).__init__(val)
        this.type = 'observable'


class ObservableArray(_Observable):

    def __init__(this, val):
        super(ObservableArray, this).__init__(val)
        this.type = 'observableArray'

    def add(this, item):
        this.value.add(item)
        this.fire('change', this)
        ui.BINDER.fire('changeFromObservable', this)

    def insert(this, index, item):
        this.value.insert(index, item)
        this.fire('change', this)
        ui.BINDER.fire('changeFromObservable', this)

    def remove(this, item):
        this.value.remove(item)
        this.fire('change', this)
        ui.BINDER.fire('changeFromObservable', this)

    def update(this, index, newItem):
        this.value.update(index, newItem)
        this.fire('change', this, index)
        ui.BINDER.fire('changeFromObservable', this, index)
