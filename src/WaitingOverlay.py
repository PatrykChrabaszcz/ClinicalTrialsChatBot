import math

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QCoreApplication, Qt, QPoint
from PyQt5.QtGui import QPalette, QPainter, QColor, QBrush, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget


# thanks to https://wiki.python.org/moin/PyQt/A%20full%20widget%20waiting%20indicator
class WaitingOverlay(QWidget):
    joystickReady = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WaitingOverlay, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.adjustSize()

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

        self.font = QtGui.QFont(QCoreApplication.instance().font())
        self.font.setPointSize(11)
        self.text = 'Querying the database…'

        self.counter = 0
        self.timer = None

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 255)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(6):
            if (self.counter // 5) % 6 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5) * 32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width() / 2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height() / 2 - 15 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20)

        painter.setPen(QPen(QtGui.QColor(0, 0, 0)))
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setFont(self.font)
        metrics = painter.fontMetrics()

        painter.drawText(
            QPoint(self.width() / 2 - metrics.width(self.text) / 2, self.height() / 2 + 60),
            self.text
        )

        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(40)
        self.counter = 0

    def hideEvent(self, event):
        if self.timer is not None:
            self.killTimer(self.timer)
            self.timer = None

    def timerEvent(self, event):
        self.counter += 1
        self.update()
