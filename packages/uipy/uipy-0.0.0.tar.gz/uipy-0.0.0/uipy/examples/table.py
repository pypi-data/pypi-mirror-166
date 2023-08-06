import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QLabel
import uipy as ui
import mupy as mu


class VM(ui.ViewModel):

    items = ui.ObservableArray(
        ui.TableModel([[{
            'text': 'Using a Component in Your Application',
            'icon': mu.myPath() + './imgs/triangle.png'
        }, {
            'text': 'Connecting widgets using a naming scheme',
            'icon': mu.myPath() + './imgs/circle.png'
        }], [{
            'text': 'Form Editing Mode'
        }, {
            'text': 'How to edit a form in Qt Designer'
        }]], ['Title', 'Description']))


ui.init()

vm = VM()

app = QApplication(sys.argv)

mw = QMainWindow()
mw.setWindowTitle("QTableView Example")
mw.setFixedSize(800, 600)
ui.center2Screen(mw)
cw = QWidget(mw)
mw.setCentralWidget(cw)
table1 = QTableView(cw)
table1.setFixedSize(640, 480)
ui.center2QMW(table1)

table1.databind = {
    'table': vm.items
}

mw.show()

vm.bind()

sys.exit(app.exec())
