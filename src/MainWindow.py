from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QTabWidget

from src.MapWidget import MapWidget
from src.DialogWidget import DialogWidget
from src.InputConsole import InputConsole
from src.DialogFlow import DialogFlow
from src.TreeWidget import TreeWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_h = QHBoxLayout()

        self.l_h_left = QHBoxLayout()
        self.l_v_middle = QVBoxLayout()
        self.l_v_right = QVBoxLayout()

        self.l_h.addLayout(self.l_h_left, 1)
        self.l_h.addLayout(self.l_v_middle, 3)
        self.l_h.addLayout(self.l_v_right, 2)

        self.map_widget = MapWidget()
        self.l_v_middle.addWidget(self.map_widget, 1)

        self.tab_widget = QTabWidget()
        self.l_h_left.addWidget(self.tab_widget, 1)

        self.disease_widget = TreeWidget("disease")
        self.tab_widget.addTab(self.disease_widget, 'Disease')

        self.drug_widget = TreeWidget("drug")
        self.tab_widget.addTab(self.drug_widget, 'Drug')

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.l_h)

        self.dialog_widget = DialogWidget()
        self.l_v_right.addWidget(self.dialog_widget)

        self.input_console = InputConsole()
        self.l_v_right.addWidget(self.input_console)

        self.dialogflow = DialogFlow()

        self.input_console.message_entered.connect(self.dialogflow.send_request)

        self.dialogflow.response_received.connect(self.dialog_widget.dialogflow_response)
        self.dialogflow.response_received.connect(self.disease_widget.dialogflow_response)
        self.dialogflow.response_received.connect(self.drug_widget.dialogflow_response)

