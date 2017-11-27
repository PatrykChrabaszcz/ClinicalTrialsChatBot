import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np

class PrintingDBConnector(QObject):
    database_response = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    # This slot is called when response is received from the DialogFlow bot
    def dialogflow_response(self, resolved_query, parameters, contexts, action):
        print(resolved_query)
        print(parameters)
        print(contexts)
        print(action)
