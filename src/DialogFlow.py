import json
import os.path
import sys
import uuid

from PyQt5.QtCore import QObject, pyqtSignal

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


class DialogFlow(QObject):
    # Emitted when DialogFlow wants to tell us something
    speak = pyqtSignal(['QString'])

    # Emitted when DialogFlow wants to query database
    # User request was successfully recognized

    query_database = pyqtSignal(['QString', dict, list, 'QString'])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ai = apiai.ApiAI('cce9915cc7f14a41b167f3251581c160')
        self.session_id = str(uuid.uuid4())

    def send_request(self, message):
        request = self.ai.text_request()
        request.session_id = self.session_id
        request.query = message
        response = json.loads(request.getresponse().read().decode('utf-8'))

        status = response['status']
        if status['code'] != 200:
            self.speak.emit('Failed to connect to the DialogFlow service.\n'
                            'Error code {0}, error type: {1}'.format(status['code'], status['errorType']))
        else:
            result = response['result']
            resolved_query = result['resolvedQuery']
            parameters = result['parameters']
            contexts = result['contexts']
            action = result['action']

            if result['actionIncomplete']:
                self.speak.emit(result['fulfillment']['speech'])
                # TODO: anything else needed?
            else:
                self.speak.emit(result['fulfillment']['speech'] + ' Querying the database…')
                self.query_database.emit(resolved_query, parameters, contexts, action)


if __name__ == '__main__':
    df = DialogFlow()
    response = df.send_request("How many Melanoma studies were started each year in Canada?")
    v = str(response).replace('\\n', '')[2:-1]

    d = json.loads(v)
    print(d['result'])
