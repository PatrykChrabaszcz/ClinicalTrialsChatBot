from PyQt5.QtCore import QObject, pyqtSignal
import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


class DialogFlow(QObject):
    response_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.ai = apiai.ApiAI('cce9915cc7f14a41b167f3251581c160')

    def send_request(self, message):
        request = self.ai.text_request()
        request.session_id = "1"
        request.query = message
        response = json.loads(request.getresponse().read().decode('utf-8'))
        self.response_received.emit(response)


if __name__ == '__main__':
    df = DialogFlow()
    response = df.send_request("How many Melanoma studies were started each year in Canada?")
    v = str(response).replace('\\n', '')[2:-1]

    d = json.loads(v)
    print(d['result'])
