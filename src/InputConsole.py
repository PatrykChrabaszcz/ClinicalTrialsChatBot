from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal


class InputConsole(QLineEdit):

    message_entered_signal = pyqtSignal('QString')

    def __init__(self, parent=None):
        super().__init__(parent)

        self.returnPressed.connect(self.message_changed)

    def message_changed(self):
        message = self.text()
        if message is "":
            return

        self.setText("")
        self.message_entered_signal.emit(message)

    def append_text(self, text):
        curr_text = self.text()
        while len(curr_text) and curr_text[-1] == " ":
            curr_text = curr_text[:-1]

        self.setText("%s %s" % (curr_text, text))



