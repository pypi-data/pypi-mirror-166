import mupy as mu
import uipy as ui
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QLabel, QButtonGroup


class Binder(ui.Dispatcher):

    # 所有绑定，内置 Databinder 对象
    databinders = []
    # 所有可观察者，内置 Observable、ObservableArray 对象
    observables = []
    # 总视图模型
    viewModel = None

    # 绑定类型
    types = {
        'value': ['str', 'int', 'float', 'bool', 'color', 'date', 'datetime', 'time'],
        'behavior': ['visible', 'enable'],
        'signal': ['click', 'dbclick', 'select'],
        'items': ['list', 'tree', 'table'],
        'select': ['selectItem', 'selectIndex', 'selectId', 'selectValue', 'selectText']
    }

    def __init__(this):
        super(Binder, this).__init__()

        this.on('changeFromObservable', this.onChangeFromObservable)
        # TODO：既然 Binder 是两者的沟通桥梁，那是不是把这个也弄过来？
        # this.on('changeFromWidget', this.onChangeFromWidget)

    def findObservable(this, uuid):
        for ob in this.observables:
            if ob[0] == uuid:
                return ob

        return None

    def findWidgetsByObservableUUID(this, uuid):
        r = []
        for db in this.databinders:
            keys = list(set(db.databind))
            for type in keys:

                # 如果绑定的是函数，就没有uuid
                if mu.isfunc(db.databind[type]):
                    continue

                if db.databind[type].uuid == uuid:
                    r.append((db.widget, type))

        return r

    def onChangeFromObservable(this, ob):

        if ui.isObservable(ob):
            # 寻找ob对应的widget，一一赋值
            ws = this.findWidgetsByObservableUUID(ob.uuid)
            val = ob.get()
            for w in ws:
                w1, type = w
                if this.types['value'].count(type) == 1:
                    if isinstance(w1, QLineEdit) or isinstance(w1, QLabel):

                        if ['int', 'float', 'bool'].count(type) == 1:
                            val = mu.toStr(val, type)
                        elif type == 'datetime':
                            val = mu.toStr(val, '%Y-%m-%d %H:%M:%S')
                        elif type == 'date':
                            val = mu.toStr(val, '%Y-%m-%d')
                        elif type == 'time':
                            val = mu.toStr(val, '%H:%M:%S')

                        w1.setText(val)

                if this.types['select'].count(type) == 1:

                    if isinstance(w1, QAbstractItemView):
                        if type == 'selectIndex':
                            w1.setCurrentIndex(val)

                    if isinstance(w1, QButtonGroup):
                        if type == 'selectId' or type == 'selectIndex':
                            ui.checkButtons(this.widget, val, type)

        elif ui.isObservableArray(ob):
            pass

    # def onChangeFromWidget(this,widget):
