import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class DatabaseConnector(QObject):
    database_response = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    # This slot is called when response is received from the DialogFlow bot
    def dialogflow_response(self, resolved_query, parameters, contexts, action):

        returns = [
            {
                "action": "compare_countries",
                "disease": "Hepatitis C",
                "phase": "Phase 2",
                "status": "active",
                "result": {
                    "Poland": 50,
                    "Germany": 25,
                    "France": 40,
                    "Finland": 80
                },
            },
            {
                "action": "compare_cities",
                "disease": "Lung Cancer",
                "status": "recruiting",
                "result": {
                    "Paris": 50,
                    "Lyon": 25,
                }

            },
            {
                "action": "compare_time",
                "disease": "Melanoma",
                "status": "started",
                "location": "Canada",
                "result": {
                    "2014": 24,
                    "2015": 60,
                    "2016": 15,
                    "2017": 25,
                }
            },
            {
                "action": "compare_countries",
                "disease": "Hepatitis C",
                "phase": "Phase 2",
                "status": "active",
                "result": {
                    "Poland": 50,
                    "Germany": 25,
                    "France": 40,
                    "Finland": 80,
                    "Sweden": 80,
                    "Japan": 80,
                    "Italy": 80,
                    "England": 80,
                    "USA": 80
                },
            },
        ]

        random_result = returns[np.random.choice([0, 1, 2, 3])]
        self.database_response.emit(random_result)
