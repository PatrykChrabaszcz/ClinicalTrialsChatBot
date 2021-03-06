from PyQt5.QtWidgets import QTextEdit
from PyQt5.Qt import QColor
import threading


class DialogWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setReadOnly(True)

        self.setTextColor(QColor(20, 20, 20))
        self.append("Write your question or look for examples (File -> Tips and Hints)")

    def user_text(self, message):
        self.setTextColor(QColor(0, 0, 0))
        self.append("User: %s" % message)

    @staticmethod
    def bot_speech(message):
        pass
        # import pyttsx3
        # engine = pyttsx3.init()
        # engine.say(message)
        # engine.runAndWait()

    def bot_text(self, message):
        thread = threading.Thread(target=DialogWidget.bot_speech, args=(message, ))
        thread.start()

        self.setTextColor(QColor(255, 0, 0))
        self.append("SimpleTrial: %s" % message)

    def user_message_entered(self, message):
        self.append('\n')
        self.user_text(message)

    def bot_message_entered(self, message):
        self.bot_text(message)

    def dialogflow_response(self, resolved_query, parameters, contexts, action):
        self.append("--")
        self.user_text(resolved_query)


