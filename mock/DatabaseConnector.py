import psycopg2
import datetime
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class DatabaseConnector(QObject):
    database_response = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    # This slot is called when response is received from the DialogFlow bot
    def dialogflow_response(self, resolved_query, parameters, contexts, action):

        returns = [
            {
                "disease": "Hepatitis C",
                "phase": "Phase 2",
                "status": "active",
                "compare_location": {
                    "Poland": 50,
                    "Germany": 25,
                    "France": 40,
                    "Finland": 80
                },
            },
            {
                "disease": "Lung Cancer",
                "status": "recruiting",
                "compare_location": {
                    "Paris": 50,
                    "Lyon": 25,
                }

            },
            {
                "disease": "Melanoma",
                "status": "started",
                "location": "Canada",
                "compare_time": {
                    "2014": 24,
                    "2015": 60,
                    "2016": 15,
                    "2017": 25,
                }
            }
        ]

        random_result = returns[np.random.choice([0,1,2])]
        self.database_response.emit(random_result)
