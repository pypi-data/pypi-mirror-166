import sys
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QListView
import uipy as ui
import mupy as mu


class VM(ui.ViewModel):

    items = ui.ObservableArray(
        ui.ListModel([{
            'text': 'Using a Component in Your Application',
            'icon': mu.myPath() + './imgs/triangle.png'
        }, {
            'text': 'Connecting widgets using a naming scheme',
            'icon': mu.myPath() + './imgs/circle.png'
        }, {
            'text': 'Form Editing Mode'
        }]))

    curText = ui.Observable('')
    curIndex = ui.Observable(QModelIndex())

    def log(this, ob):
        print(ob.get())

    def __init__(this):
        super(VM, this).__init__()

        this.curText.on('change', this.log)
        this.curIndex.on('change', this.log)


ui.init()

vm = VM()

app = QApplication(sys.argv)

print(mu.myPath())

mw = QMainWindow()
mw.setWindowTitle("QListView Example")
mw.setFixedSize(800, 600)
ui.center2Screen(mw)
cw = QWidget(mw)
mw.setCentralWidget(cw)
list1 = QListView(cw)
list1.setFixedSize(640, 480)
ui.center2QMW(list1)

list1.databind = {
    'list': vm.items,
    'selectText': vm.curText,
    'selectIndex': vm.curIndex
}

mw.show()

vm.bind()

sys.exit(app.exec())
