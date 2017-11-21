from PyQt5.QtWidgets import QTextEdit


class DialogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(150)
        self.setReadOnly(True)

        self.user_text("How many Hepatitis C studies (Phase 2) are active in each country")
        self.bot_text("I think it's 20")

    def user_text(self, message):
        self.append("User: \t%s \n" % message)

    def bot_text(self, message):
        self.append("Bot: \t%s \n" % message)
