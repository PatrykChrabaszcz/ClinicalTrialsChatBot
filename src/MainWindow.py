from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QTabWidget

from src.MapWidget import MapWidget
from src.DialogWidget import DialogWidget
from src.InputConsole import InputConsole
from src.DialogFlow import DialogFlow
from src.ResponseParser import ResponseParser
from src.ViewTree import ViewTree, DiseaseView

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.l_h = QHBoxLayout()

        self.l_v_left = QVBoxLayout()
        self.l_v_right = QVBoxLayout()

        self.l_h.addLayout(self.l_v_left, 1)
        self.l_h.addLayout(self.l_v_right, 1)

        self.map_widget = MapWidget()
        self.l_v_left.addWidget(self.map_widget, 1)

        self.tab_widget = QTabWidget()
        self.l_v_left.addWidget(self.tab_widget, 1)

        self.disease_view = DiseaseView()
        self.tab_widget.addTab(self.disease_view, 'Disease')

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.l_h)

        self.dialog_widget = DialogWidget()
        self.l_v_right.addWidget(self.dialog_widget)

        self.input_console = InputConsole()
        self.l_v_right.addWidget(self.input_console)

        self.dialogflow = DialogFlow()
        self.response_parser = ResponseParser()

        self.input_console.message_entered.connect(self.dialog_widget.user_message_entered)
        self.input_console.message_entered.connect(self.dialogflow.send_request)
        # self.dialogflow.response_received.connect(self.dialog_widget.bot_message_entered)
        #self.dialogflow.response_received.connect(self.response_parser.parse_response)




