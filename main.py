import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow
from book_window import Ui_BookWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.searchButton.clicked.connect(self.open_book)

    def open_book(self):
        self.book = BookText()
        self.book.show()


class BookText(QMainWindow, Ui_BookWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('book_window.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
