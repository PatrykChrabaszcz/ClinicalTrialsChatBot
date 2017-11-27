from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QTabWidget, QScrollArea, QSizePolicy
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtCore import QSize
from src.MapWidget import MapWidget
from src.DialogWidget import DialogWidget
from src.InputConsole import InputConsole
from src.DialogFlow import DialogFlow
from src.TreeWidget import TreeWidget
from src.ChartWidget import ChartWidget
from src.DatabaseConnector import DatabaseConnector


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCentralWidget(QWidget(self))
        self.l_h = QHBoxLayout(self.centralWidget())

        # Initialize all components
        self.map_widget = MapWidget(self.centralWidget())
        self.chart_widget = ChartWidget(self.centralWidget())
        self.disease_widget = TreeWidget("disease", self.centralWidget())
        self.drug_widget = TreeWidget("drug", self.centralWidget())
        self.dialog_widget = DialogWidget(self.centralWidget())
        self.input_console = InputConsole(self.centralWidget())
        self.dialogflow = DialogFlow(self)
        self.database_connector = DatabaseConnector(self)

        # Arrange components in a layout
        self.l_h_left = QHBoxLayout()
        self.l_v_middle = QVBoxLayout()
        self.l_v_right = QVBoxLayout()

        self.l_h.addLayout(self.l_h_left, 1)
        self.l_h.addLayout(self.l_v_middle, 3)
        self.l_h.addLayout(self.l_v_right, 2)

        self.tab_widget_visualization = QTabWidget(self.centralWidget())
        self.scroll_area = QScrollArea(self.centralWidget())
        self.scroll_area.setWidget(self.chart_widget)
        self.scroll_area.setWidgetResizable(True)
        self.tab_widget_visualization.addTab(self.scroll_area, 'Chart')
        self.tab_widget_visualization.addTab(self.map_widget, 'Map')
        self.l_v_middle.addWidget(self.tab_widget_visualization)

        self.l_v_right.addWidget(self.dialog_widget)
        self.l_v_right.addWidget(self.input_console)

        self.tab_widget = QTabWidget(self.centralWidget())
        self.tab_widget.addTab(self.disease_widget, 'Disease')
        self.tab_widget.addTab(self.drug_widget, 'Drug')

        self.l_h_left.addWidget(self.tab_widget, 1)
        # Declare interaction between the components
        self.input_console.message_entered_signal.connect(self.dialog_widget.user_message_entered)
        self.input_console.message_entered_signal.connect(self.dialogflow.send_request)

        # Highlight diseases and drugs for which we search in the database
        self.dialogflow.query_database.connect(self.disease_widget.dialogflow_response)
        self.dialogflow.query_database.connect(self.drug_widget.dialogflow_response)

        # Query the database
        self.dialogflow.speak.connect(self.dialog_widget.bot_message_entered)
        self.dialogflow.query_database.connect(self.database_connector.dialogflow_response)

        # Display query on the chart and on the map
        self.database_connector.database_response.connect(self.map_widget.database_response)
        self.database_connector.database_response.connect(self.chart_widget.database_response)

        self.disease_widget.element_selected.connect(self.input_console.append_text)
        self.drug_widget.element_selected.connect(self.input_console.append_text)

