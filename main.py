import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    window.hint_window.show()
    app.exec()

if __name__ == "__main__":
    main()
