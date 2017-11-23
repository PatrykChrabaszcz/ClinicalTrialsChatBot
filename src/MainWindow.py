from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit

from src.MapWidget import MapWidget
from src.DialogWidget import DialogWidget
from src.InputConsole import InputConsole
from src.DialogFlow import DialogFlow
from src.ResponseParser import ResponseParser


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.l = QVBoxLayout()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.l)

        self.map_widget = MapWidget()
        self.l.addWidget(self.map_widget)
        self.setLayout(self.l)

        self.dialog_widget = DialogWidget()
        self.l.addWidget(self.dialog_widget)

        self.input_console = InputConsole()
        self.l.addWidget(self.input_console)

        self.dialogflow = DialogFlow()
        self.response_parser = ResponseParser()

        self.input_console.message_entered.connect(self.dialog_widget.user_message_entered)
        self.input_console.message_entered.connect(self.dialogflow.send_request)
        #self.dialogflow.response_received.connect(self.dialog_widget.bot_message_entered)
        self.dialogflow.response_received.connect(self.response_parser.parse_response)




