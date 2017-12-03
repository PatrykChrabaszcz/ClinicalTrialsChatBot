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
    bot_speak_signal = pyqtSignal('QString')

    # Emitted when DialogFlow returns user message
    # DialogFlow can recognize speech
    user_speak_signal = pyqtSignal('QString')

    # Emitted when DialogFlow wants to query database
    # User request was successfully recognized
    bot_request_signal = pyqtSignal(['QString', dict, list, 'QString'])

    def __init__(self, parent=None):
        super().__init__(parent)
        # New session every time we start the program
        self.ai = apiai.ApiAI('cce9915cc7f14a41b167f3251581c160')
        self.session_id = str(uuid.uuid4())

    # Slot that should be connected to the signal from the user interface
    # Will use DialogFlow API to analyze request
    def process_user_message(self, message):
        # Send request and get a response
        request = self.ai.text_request()
        request.session_id = self.session_id
        request.query = message
        response = json.loads(request.getresponse().read().decode('utf-8'))

        status = response['status']
        if status['code'] != 200:
            self.bot_speak_signal.emit('Failed to connect to the DialogFlow service.\n'
                                       'Error code {0}, error type: {1}'.format(status['code'], status['errorType']))
        else:
            result = response['result']
            resolved_query = result['resolvedQuery']
            parameters = result['parameters']
            contexts = result['contexts']
            action = result['action']

            self.user_speak_signal.emit(resolved_query)
            self.bot_speak_signal.emit(result['fulfillment']['speech'])

            if not result['actionIncomplete']:
                if action != 'input.unknown':
                    if '.next' not in action:
                        self.bot_request_signal.emit(resolved_query, parameters, contexts, action)
                    else:
                        action = action.split('.')[0]
                        if len(contexts) > 0:
                            parameters = self._merge_from_context(parameters, contexts[0])
                            self.bot_request_signal.emit(resolved_query, parameters, contexts, action)
                        else:
                            self.bot_speak_signal.emit('Unknown error.\n')

    # noinspection PySimplifyBooleanCheck,PyMethodMayBeStatic
    def _merge_from_context(self, parameters, context):
        parameters_merged = {}

        # take followup intent params, replacing their original values if specified
        for p in parameters:
            original_p = p[:-5]
            parameters_merged[original_p] = context['parameters'][original_p]
            if (isinstance(parameters[p], list) and parameters[p] != []) \
                    or (isinstance(parameters[p], str) and parameters[p] != ''):
                parameters_merged[original_p] = parameters[p]

        # carry over any other params originally present
        for p in context['parameters']:
            if p.endswith('.original') or p.endswith('_next'):
                continue
            else:
                if p not in parameters_merged:
                    parameters_merged[p] = context['parameters'][p]

        # override the location with new data for the Compare intent
        if 'geo-country_next' in parameters and 'geo-city_next' in parameters:
            if parameters['geo-country_next'] != []:
                parameters_merged['geo-city'] = []
            elif parameters['geo-city_next'] != []:
                parameters_merged['geo-country'] = []

        return parameters_merged


if __name__ == '__main__':
    df = DialogFlow()
    response = df.send_request("How many Melanoma studies were started each year in Canada?")
    v = str(response).replace('\\n', '')[2:-1]

    d = json.loads(v)
    print(d['result'])
