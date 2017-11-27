from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence, QKeyEvent


class InputConsole(QLineEdit):
    class MessageHistory:
        def __init__(self):
            self.history = []
            self.index = 0

        def reset(self):
            self.index = len(self.history)

        def current_message(self):
            return (self.history + [""])[self.index]

        def up(self):
            self.index = max(0, self.index-1)

            return self.current_message()

        def down(self):
            self.index = min(len(self.history), self.index + 1)

            return self.current_message()

        def append_message(self, message):
            self.history.append(message)
            self.reset()

    message_entered_signal = pyqtSignal('QString')

    def __init__(self, parent=None):
        super().__init__(parent)

        self.history = InputConsole.MessageHistory()
        self.returnPressed.connect(self.message_changed)

    def message_changed(self):
        message = self.text()
        if message is "":
            return

        self.setText("")
        self.message_entered_signal.emit(message)
        self.history.append_message(message)

    def append_text(self, text):
        curr_text = self.text()
        while len(curr_text) and curr_text[-1] == " ":
            curr_text = curr_text[:-1]

        self.setText("%s %s" % (curr_text, text))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.setText(self.history.up())
        elif event.key() == Qt.Key_Down:
            self.setText(self.history.down())
        elif event.matches(QKeySequence.Copy):
            self.history.reset()
            self.setText("")
        else:
            super().keyPressEvent(event)

