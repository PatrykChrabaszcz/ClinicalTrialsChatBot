from PyQt5.QtWidgets import QTextEdit
from PyQt5.Qt import QColor
import os
from multiprocessing import Pool


class DialogWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setReadOnly(True)
        self.pool = Pool(processes=1)

        self.user_text("How many Hepatitis C studies (Phase 2) are in each country")
        self.bot_text("I think it's 20")

    def user_text(self, message):
        self.setTextColor(QColor(255, 0, 0))
        self.append("User: \t%s" % message)

    @staticmethod
    def bot_speech(message):
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

    def bot_text(self, message):
        self.pool.apply_async(DialogWidget.bot_speech, [message])

        self.setTextColor(QColor(0, 0, 255))
        self.append("Bot: \t%s" % message)

    def user_message_entered(self, message):
        self.user_text(message)

    def bot_message_entered(self, message):
        self.bot_text(message)

    def dialogflow_response(self, resolved_query, parameters, contexts, action):
        self.user_text(resolved_query)
