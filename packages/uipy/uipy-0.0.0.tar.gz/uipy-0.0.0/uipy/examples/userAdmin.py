import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLayout
from PySide6.QtCore import QDate, QDateTime, QTime, Qt
from PySide6.QtGui import QPainter, QPen, QColor
from userAdminUI import Ui_MainWindow
import uipy as ui


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui1 = Ui_MainWindow()
        self.ui1.setupUi(self)

        ui.QMW = self

        self.ui1.radiobuttonGroup1.databind = {
            'radioGroup': vm.genders,
            'selectId': vm.user.gender
        }

        self.ui1.checkboxGroup1.databind = {
            'checkboxGroup': vm.favorites,
            'selectId': vm.user.favorites
        }

        self.ui1.comboBox1.databind = {
            'list': vm.educations,
            'selectValue': vm.user.education
        }


class User:
    username = ''
    age = 0
    birth = QDate()
    birth2 = QDateTime()
    birthHour = QTime()
    gender = 1
    favorites = [1, 2]
    education = 'college'
    kongfu = 60


class VM(ui.ViewModel):
    user = ui.fromObj(User())

    genders = ui.ObservableArray(ui.ListModel([{
        'id': 0,
        'text': '女性'
    }, {
        'id': 1,
        'text': '男性'
    }]))

    favorites = ui.ObservableArray(ui.ListModel([{
        'id': 0,
        'text': '电影'
    }, {
        'id': 1,
        'text': '音乐'
    }, {
        'id': 2,
        'text': '游戏'
    }, {
        'id': 3,
        'text': '体育'
    }]))

    educations = ui.ObservableArray(ui.ListModel([{
        'text': '博士',
        'value': 'doctor'
    }, {
        'text': '硕士',
        'value': 'master'
    }, {
        'text': '本科',
        'value': ' bachelor'
    }]))


if __name__ == "__main__":

    ui.init()

    vm = VM()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    vm.bind()

    sys.exit(app.exec())
