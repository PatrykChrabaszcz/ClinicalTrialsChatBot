from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import QSize


class HintWindow(QWidget):
    class HintMessages:
        def __init__(self):
            self.messages = []
            self.counter = 0
            self.messages.append('You can simply double click on the disease or drug name in the left panel '
                                 'to copy it into the input console.')
            self.messages.append('You can ask the bot to compare number of studies for a particular disease between '
                                 'the countries. Try: \n\"How many Hepatitis C studies (Phase 2) are in each country\"')
            self.messages.append('When you ask the bot to compare studies in different regions or different cities, '
                                 'then he has to query Google Maps API for each location, this might take a while. '
                                 'Be patient."')
            self.messages.append('Try out: "Count Eye Diseases studies in 2015 and 2016 in Germany and Poland"')

            self.messages.append('Try out: "Compare Neoplasm studies Phase 1 in different regions of Poland"')

            self.messages.append('Try out: "Compare Recruiting Neoplasm studies Phase 1 in different regions of Poland"')

        def current(self):
            return self.messages[self.counter]

        def next(self):
            self.counter = (self.counter + 1) % len(self.messages)
            return self.messages[self.counter]

        def previous(self):
            self.counter = (self.counter - 1) % len(self.messages)
            return self.messages[self.counter]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hint_messages = HintWindow.HintMessages()

        self.setWindowTitle('Did you know?')

        self.resize(QSize(300, 200))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.next_button = QPushButton(self)
        self.next_button.setText('Next')
        self.next_button.pressed.connect(self.display_next)

        self.prev_button = QPushButton(self)
        self.prev_button.setText('Prev')
        self.prev_button.pressed.connect(self.display_prev)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)

        self.text_field = QTextEdit()
        self.text_field.setReadOnly(True)
        self.text_field.setText(self.hint_messages.current())

        self.layout.addWidget(self.text_field)
        self.layout.addLayout(self.button_layout)

    def display_next(self):
        self.text_field.setText(self.hint_messages.next())

    def display_prev(self):
        self.text_field.setText(self.hint_messages.next())
