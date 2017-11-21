from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit

from src.MapWidget import MapWidget
from src.DialogWidget import DialogWidget
from src.InputConsole import InputConsole


class MainWindow(QMainWindow):
    def __init__(self, cache_dir, parent=None):
        super().__init__(parent)
        self.l = QVBoxLayout()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.l)

        self.map_widget = MapWidget(cache_dir)
        self.l.addWidget(self.map_widget)
        self.setLayout(self.l)

        self.dialog_widget = DialogWidget()
        self.l.addWidget(self.dialog_widget)

        self.input_console = InputConsole()
        self.l.addWidget(self.input_console)





