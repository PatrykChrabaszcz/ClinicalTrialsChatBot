import sys
from PyQt5.QtWidgets import QApplication

from src.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 600)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
