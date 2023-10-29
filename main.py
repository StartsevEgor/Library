import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow
from book_window import Ui_BookWindow
from library import Library


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.initUI()

    def new_library(self):
        self.lib.save()
        self.lib = Library()
        self.lib.make()

    def initUI(self):
        if not os.path.isdir("Last library"):
            self.lib = Library()
            self.lib.make()
        else:
            self.lib = Library()
            self.lib.open()
        self.actionNew_library.triggered.connect(self.new_library)

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
