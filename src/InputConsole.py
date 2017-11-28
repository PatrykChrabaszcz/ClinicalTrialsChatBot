from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence


# Widget used by the user to enter queries to the system
class InputConsole(QLineEdit):
    # Signal emitted when user submits a new query
    # This should be sent to the DialogFlow Bot
    user_message_entered_signal = pyqtSignal('QString')

    # Simple class to handle message history,
    # User can use Up/Down Arrow keys to search for
    # commands already entered in this session
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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.history = InputConsole.MessageHistory()
        self.returnPressed.connect(self.message_changed)
        self.setPlaceholderText("Please insert your question.")

    def message_changed(self):
        message = self.text()
        if message is "":
            return
        self.setText("")
        self.user_message_entered_signal.emit(message)
        self.history.append_message(message)

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


