import os

from zipfile import ZipFile
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow
from book_window import Ui_BookWindow
from library import Library


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        if not os.path.isdir("Last library"):
            if os.path.isfile("last_libraries.txt"):
                self.last_libraries = open("last_libraries.txt", "r").readlines()  # список последних открытых библиотек
                self.last_library = self.last_libraries[-1][:-1]

                os.mkdir("Last library")
                os.rename(self.last_library, self.last_library[:-3] + "zip")
                self.last_library = self.last_library[:-3] + "zip"

                # Распаковка последней библиотеки в отдельную папку для более комфортной работы с ней
                ZipFile(self.last_library, "r").extractall(path="Last library")
            else:
                self.last_libraries = open("last_libraries.txt", "w")
                self.last_libraries.write("Library.lib\n")


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
