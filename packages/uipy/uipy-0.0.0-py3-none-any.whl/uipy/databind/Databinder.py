import mupy as mu
import uipy as ui
from PySide6.QtWidgets import QAbstractItemView, QLineEdit, QLabel, QListView, QTreeView, QTableView, QButtonGroup, QComboBox, QRadioButton, QCheckBox
from PySide6.QtCore import Qt
import uuid as uid


class Databinder(ui.Dispatcher):

    databind = None
    widget = None

    def __init__(this, widget):
        super(Databinder, this).__init__()
        this.widget = widget
        this.widget.uuid = uid.uuid4().hex
        if hasattr(this.widget, 'databind'):
            this.databind = this.widget.databind

    def _onSelect(this, selected, deselected):
        index = selected.indexes()[0]
        keys = mu.getProperties(this.databind)
        for type in keys:
            ob = this.databind[type]

            if type == 'selectItem':
                ob.set(index.data(Qt.UserRole))

            if type == 'selectValue':
                ob.set(index.data(Qt.UserRole)['value'])

            if type == 'selectId':
                ob.set(index.data(Qt.UserRole)['id'])

            if type == 'selectIndex':
                if isinstance(this.widget, QAbstractItemView):
                    ob.set(index)

            if type == 'selectText':
                ob.set(index.data(Qt.DisplayRole))

    def _onGroupButtonSelect(this, item):
        grp = item.group()
        idxs = []
        items = []
        indexes = []
        texts = []

        for i, btn in enumerate(grp.buttons()):
            if btn.isChecked():
                id = grp.id(btn)
                text = btn.text()
                texts.append(text)
                idxs.append(id)
                indexes.append(i)
                items.append({
                    'id': id,
                    'text': text
                })

        keys = mu.getProperties(this.databind)
        for type in keys:
            ob = this.databind[type]

            if type == 'selectItem':
                ob.set(items)

            if type == 'selectId':
                ob.set(idxs)

            if type == 'selectIndex':
                ob.set(indexes)

            if type == 'selectText':
                ob.set(texts)

    def _onEditingFinished(this):
        if mu.isN(this.databind):
            return

        # TODO:还有别的类型控件
        if isinstance(this.widget, QLineEdit) or isinstance(this.widget, QLabel):
            keys = mu.getProperties(this.databind)
            for type in keys:
                ob = this.databind[type]
                if ui.BINDER.types['value'].count(type) == 1:
                    ob.set(this.widget.text())

    def _connectSignal(this):

        if isinstance(this.widget, QLineEdit):
            this.widget.on(this.widget.editingFinished, this._onEditingFinished)

        if isinstance(this.widget, QListView):
            # 注意，selectionModel() 必须有在设定 listview.setMode 之后，否则返回空
            this.widget.on(this.widget.selectionModel().selectionChanged, this._onSelect)

        if isinstance(this.widget, QButtonGroup):
            this.widget.on(this.widget.buttonClicked, this._onGroupButtonSelect)

    def _bindSignal(this):
        keys = mu.getProperties(this.databind)
        for type in keys:
            fn = this.databind[type]
            # TODO:还有更多事件
            if type == 'click':
                this.widget.on(this.widget.clicked, fn)

            if type == 'select':

                if isinstance(this.widget, QListView) or isinstance(this.widget, QTreeView) or isinstance(this.widget, QTableView):
                    this.widget.on(this.widget.selectionModel().selectionChanged, fn)

                if isinstance(this.widget, QButtonGroup):
                    this.widget.on(this.widget.buttonClicked, fn)

    def _bindItems(this):
        keys = mu.getProperties(this.databind)
        for type in keys:
            ob = this.databind[type]

            if type == 'list':
                if isinstance(this.widget, QListView) or isinstance(this.widget, QComboBox):
                    this.widget.setModel(ob.get())

            elif type == 'tree':
                if isinstance(this.widget, QTreeView):
                    this.widget.setModel(ob.get())

            elif type == 'table':
                if isinstance(this.widget, QTableView):
                    this.widget.setModel(ob.get())

            elif type == 'radioGroup':
                if isinstance(this.widget, QButtonGroup):
                    items = ob.get().items
                    ui.addButtonsToGroup(items, this.widget, ui.QMW.centralWidget(), 'radio')

            elif type == 'checkboxGroup':
                if isinstance(this.widget, QButtonGroup):
                    items = ob.get().items
                    ui.addButtonsToGroup(items, this.widget, ui.QMW.centralWidget(), 'checkbox')

    def _initValue(this):
        if mu.isN(this.databind):
            return

        keys = mu.getProperties(this.databind)
        for type in keys:

            ob = this.databind[type]

            if isinstance(this.widget, QLineEdit) or isinstance(this.widget, QLabel):
                if ui.BINDER.types['value'].count(type) == 1:
                    ui.BINDER.fire('changeFromObservable', ob)

            if isinstance(this.widget, QButtonGroup):
                if type == 'selectId' or type == 'selectIndex':
                    ui.checkButtons(this.widget, ob.get(), type)

    def bind(this):
        if mu.isN(this.databind):
            return

        ui.BINDER.databinders.append(this)

        this._bindItems()

        this._connectSignal()

        this._bindSignal()

        this._initValue()
