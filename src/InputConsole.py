from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal


class InputConsole(QLineEdit):
    message_entered = pyqtSignal('QString')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnPressed.connect(self.message_changed)

    def message_changed(self):
        message = self.text()
        if message is "":
            return

        self.setText("")
        self.message_entered.emit(message)


