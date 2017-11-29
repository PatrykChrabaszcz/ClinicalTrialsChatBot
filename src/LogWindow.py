from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class Logger:
    def __init__(self):
        self.log_window = None

    def set_log_window(self, log_window):
        self.log_window = log_window

    def log(self, message):
        if self.log_window is not None:
            self.log_window.log(message)


class LogWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Logs')
        self.logs = []

        self.layout = QVBoxLayout(self)
        self.text_field = QTextEdit()
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field)

    def log(self, message):
        # TODO: ADD time and LVL
        self.text_field.append(message)

logger = Logger()
