# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userAdmin.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QDateEdit, QDateTimeEdit, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QListView, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QSpinBox, QStatusBar, QTimeEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout_3.addWidget(self.listView)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit1 = QLineEdit(self.centralwidget)
        self.lineEdit1.setObjectName(u"lineEdit1")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEdit1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.spinBox1 = QSpinBox(self.centralwidget)
        self.spinBox1.setObjectName(u"spinBox1")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.spinBox1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.dateEdit1 = QDateEdit(self.centralwidget)
        self.dateEdit1.setObjectName(u"dateEdit1")
        self.dateEdit1.setDate(QDate(1979, 12, 31))

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.dateEdit1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.dateTimeEdit1 = QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit1.setObjectName(u"dateTimeEdit1")
        self.dateTimeEdit1.setDateTime(QDateTime(QDate(1979, 1, 1), QTime(0, 0, 0)))
        self.dateTimeEdit1.setTimeSpec(Qt.LocalTime)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.dateTimeEdit1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.timeEdit1 = QTimeEdit(self.centralwidget)
        self.timeEdit1.setObjectName(u"timeEdit1")
        self.timeEdit1.setTime(QTime(12, 0, 0))

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.timeEdit1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton = QRadioButton(self.centralwidget)
        self.radiobuttonGroup1 = QButtonGroup(MainWindow)
        self.radiobuttonGroup1.setObjectName(u"radiobuttonGroup1")
        self.radiobuttonGroup1.addButton(self.radioButton)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radiobuttonGroup1.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout.addWidget(self.radioButton_2)


        self.formLayout_2.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkboxGroup1 = QButtonGroup(MainWindow)
        self.checkboxGroup1.setObjectName(u"checkboxGroup1")
        self.checkboxGroup1.setExclusive(False)
        self.checkboxGroup1.addButton(self.checkBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkboxGroup1.addButton(self.checkBox)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)


        self.formLayout_2.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_8)

        self.comboBox1 = QComboBox(self.centralwidget)
        self.comboBox1.setObjectName(u"comboBox1")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.comboBox1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.label_9)

        self.progressBar1 = QProgressBar(self.centralwidget)
        self.progressBar1.setObjectName(u"progressBar1")
        self.progressBar1.setValue(60)

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.progressBar1)


        self.horizontalLayout_3.addLayout(self.formLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton1 = QPushButton(self.centralwidget)
        self.pushButton1.setObjectName(u"pushButton1")

        self.horizontalLayout_4.addWidget(self.pushButton1)

        self.pushButton2 = QPushButton(self.centralwidget)
        self.pushButton2.setObjectName(u"pushButton2")

        self.horizontalLayout_4.addWidget(self.pushButton2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u7ba1\u7406", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u59d3\u540d\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5e74\u9f84\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u51fa\u751f\u65e5\u671f\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u51fa\u751f\u65e5\u671f2\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u51fa\u751f\u65f6\u8fb0\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u6027\u522b\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u559c\u597d\uff1a", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u5b66\u5386\uff1a", None))
        self.comboBox1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u529f\u592b\u7b49\u7ea7\uff1a", None))
        self.pushButton1.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u589e", None))
        self.pushButton2.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
    # retranslateUi

