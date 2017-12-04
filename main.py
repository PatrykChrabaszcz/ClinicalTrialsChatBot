import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import src.utils as utils
from src.MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(utils.find_data_file("icon.png")))
    window = MainWindow()
    window.showMaximized()
    window.hint_window.show()
    app.exec()

if __name__ == "__main__":
    main()
