import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeView, QLabel
import uipy as ui
import mupy as mu


class VM(ui.ViewModel):

    items = ui.ObservableArray(
        ui.TreeModel([{
            'text': ['Using a Component in Your Application', 'Generating code from forms'],
            'icon': [mu.myPath() + './imgs/triangle.png', mu.myPath() + './imgs/circle.png'],
            'children': [{
                'text': ['Automatic Connections', 'Connecting widgets using a naming scheme'],
                'icon': mu.myPath() + './imgs/circle.png',
                'children': [{
                    'text': ['A Dialog Without Auto-Connect', 'How to connect widgets without a naming scheme'],
                    'icon': mu.myPath() + './imgs/rect.png'
                }]
            }]
        }, {
            'text': ['Form Editing Mode', 'How to edit a form in Qt Designer']
        }], ['Title', 'Description']))


ui.init()

vm = VM()

app = QApplication(sys.argv)

mw = QMainWindow()
mw.setWindowTitle("QTreeView Example")
mw.setFixedSize(800, 600)
ui.center2Screen(mw)
cw = QWidget(mw)
mw.setCentralWidget(cw)
tree = QTreeView(cw)
tree.setFixedSize(640, 480)
ui.center2QMW(tree)

tree.databind = {
    'tree': vm.items
}

mw.show()

vm.bind()

sys.exit(app.exec())
