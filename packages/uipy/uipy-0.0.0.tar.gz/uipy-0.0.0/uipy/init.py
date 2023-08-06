from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLineEdit, QLabel
import uipy as ui

global QMW
QMW = None
global BINDER
BINDER = ui.Binder()


def init():
    ui.UncaughtHook()
