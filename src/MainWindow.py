from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QTabWidget

from src.MapWidget import MapWidget
from src.DialogWidget import DialogWidget
from src.InputConsole import InputConsole
from src.DialogFlow import DialogFlow
from src.TreeWidget import TreeWidget
from src.ChartWidget import ChartWidget
from mock.DatabaseConnector import DatabaseConnector


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCentralWidget(QWidget(self))
        self.l_h = QHBoxLayout(self.centralWidget())

        self.l_h_left = QHBoxLayout()
        self.l_v_middle = QVBoxLayout()
        self.l_v_right = QVBoxLayout()

        self.l_h.addLayout(self.l_h_left, 1)
        self.l_h.addLayout(self.l_v_middle, 3)
        self.l_h.addLayout(self.l_v_right, 2)

        self.map_widget = MapWidget()
        self.l_v_middle.addWidget(self.map_widget, 2)

        self.chart_widget = ChartWidget()
        self.l_v_middle.addWidget(self.chart_widget, 1)

        self.tab_widget = QTabWidget()
        self.l_h_left.addWidget(self.tab_widget, 1)

        self.disease_widget = TreeWidget("disease")
        self.tab_widget.addTab(self.disease_widget, 'Disease')

        self.drug_widget = TreeWidget("drug")
        self.tab_widget.addTab(self.drug_widget, 'Drug')

        self.dialog_widget = DialogWidget()
        self.l_v_right.addWidget(self.dialog_widget)

        self.input_console = InputConsole()
        self.l_v_right.addWidget(self.input_console)

        self.dialogflow = DialogFlow()

        self.input_console.message_entered_signal.connect(self.dialog_widget.user_message_entered)
        self.input_console.message_entered_signal.connect(self.dialogflow.send_request)

        self.database_connector = DatabaseConnector()

        self.dialogflow.speak.connect(self.dialog_widget.bot_message_entered)

        # Highlight diseases and drugs for which we search in the database
        self.dialogflow.query_database.connect(self.disease_widget.dialogflow_response)
        self.dialogflow.query_database.connect(self.drug_widget.dialogflow_response)

        # Query the database
        self.dialogflow.query_database.connect(self.database_connector.dialogflow_response)

        self.database_connector.database_response.connect(self.map_widget.database_response)

        self.disease_widget.element_selected.connect(self.input_console.append_text)
        self.drug_widget.element_selected.connect(self.input_console.append_text)

