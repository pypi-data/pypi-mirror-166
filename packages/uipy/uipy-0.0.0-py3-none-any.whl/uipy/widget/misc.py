from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
import uipy as ui


def drawRectOfLayout(painter, parent=None):
    """对Layout绘制矩形

    Args:
        painter (QPainter): 绘画器
        parent (QLayout, optional): 父布局. Defaults to None.
    """

    def drawRect(item):
        pen = QPen(QColor(Qt.red))
        pen.setStyle(Qt.DashDotLine)
        painter.setPen(pen)
        painter.drawRect(item.geometry())

    ui.eachChildLayout(drawRect, parent)
