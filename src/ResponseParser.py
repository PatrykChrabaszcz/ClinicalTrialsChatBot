from PyQt5.QtCore import pyqtSignal, QObject


# Class to parse response from the DialogFlow, based on the response type
# correct database function is called.
class ResponseParser(QObject):
    message_entered = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def parse_response(self, response):
        print(response)
        # Extracts response components


