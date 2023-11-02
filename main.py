import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from main_window import Ui_MainWindow
from book_window import Ui_BookWindow
from choice_book_window import Ui_ChoiceBookWindow
from library import Library


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.initUI()

    def initUI(self):
        if not os.path.isdir("Last library"):
            self.lib = Library()
            self.lib.make()
        else:
            self.lib = Library(flag_new_file=False)
            self.lib.open()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")
        self.actionNew_library.triggered.connect(self.new_library)
        self.actionOpen.triggered.connect(self.open_library)
        self.actionOpenLastLibraries.triggered.connect(self.open_last_libraries)
        self.actionSave.triggered.connect(self.lib.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionRename.triggered.connect(self.rename)
        self.actionDelete.triggered.connect(self.delete)
        self.actionAdd_book.triggered.connect(self.open_choice_book)
        self.searchButton.clicked.connect(self.search)

    def add_book(self):
        file = QFileDialog.getOpenFileName(self, "Выбрать книгу", "", "Книга (*.txt)")[0]

    def search(self):
        search_by_author = self.authorEdit.setText() if self.authorEdit.setText() else "*"
        search_by_title = self.titleEdit.setText() if self.titleEdit.setText() else "*"
        search_by_year = self.yearEdit.setText() if self.yearEdit.setText() else "*"
        search_by_genre = self.genreEdit.setText() if self.genreEdit.setText() else "*"

    def delete(self):
        os.remove(self.lib.name.strip())
        with open("last_libraries.txt", "r") as f:
            libraries = f.readlines()
        os.remove("last_libraries.txt")
        with open("last_libraries.txt", "w") as f:
            f.writelines(libraries[:-1])
        if len(libraries) > 1:
            self.lib = Library(flag_new_file=False)
            self.lib.open()
        else:
            self.lib = Library()
            self.lib.open()

    def rename(self):
        new_name, ok_pressed = QInputDialog.getText(self, "Переименовать", "Введите новое имя:")
        if ok_pressed:
            self.lib.name = "/".join(self.lib.name.split("/")[:-1]) + "/" + new_name + ".lib"
            with open("last_libraries.txt", "r") as f:
                last_libraries = f.readlines()
                os.remove(last_libraries[-1].strip())
            os.remove("last_libraries.txt")
            with open("last_libraries.txt", "w") as f:
                f.writelines(last_libraries[:-1])
            self.lib.save()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")

    def save_as(self):
        with open("last_libraries.txt", "r") as libraries:
            last_directory = "/".join(libraries.readlines()[-1].split("/")[:-1])
        file = QFileDialog.getSaveFileName(self, "Сохранить", last_directory,
                                           "Библиотека (*.lib);;Сжатая папка(*.zip)")[0]
        os.remove(self.lib.name.strip())
        self.lib.name = file
        with open("last_libraries.txt", "r") as f:
            last_libraries = f.readlines()
        os.remove("last_libraries.txt")
        with open("last_libraries.txt", "w") as f:
            f.writelines(last_libraries[:-1])
        self.lib.save()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")

    def new_library(self):
        self.lib.save()
        self.lib = Library()
        self.lib.make()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")

    def open_library(self):
        with open("last_libraries.txt", "r") as libraries:
            last_directory = "/".join(libraries.readlines()[-1].split("/")[:-1])
        file_name = QFileDialog.getOpenFileName(self, "Выбрать библиотеку", last_directory,
                                                "Библиотека (*.lib);;Сжатая папка(*.zip)")[0]
        if file_name:
            self.lib.save()
            self.lib = Library(file_name.strip(), flag_new_file=False)
            self.lib.open()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")

    def open_last_libraries(self):
        with open("last_libraries.txt", "r") as libraries:
            libraries = list(map(lambda x: x.strip(), libraries.readlines()))
        library, ok_pressed = (
            QInputDialog.getItem(self, "Выбрать библиотеку", "Выберите библиотеку", libraries, 1, False))
        if ok_pressed:
            self.lib.save()
            self.lib = Library(library.strip(), flag_new_file=False)
            self.lib.open()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")

    def open_book(self):
        self.book = BookText()
        self.book.show()

    def open_choice_book(self):
        self.choice_book = ChoiceBook()
        self.choice_book.show()
        self.choice_book.add_bookButton.clicked.connect(self.set_data)
        self.choice_book.cancelButton.clicked.connect(self.choice_book.close)

    def set_data(self):
        self.flag, self.author, self.title, self.year, self.text, self.picture = self.choice_book.initUI()
        print(self.author, self.title, self.year, self.text, self.picture)
        if self.flag:
            self.choice_book.close()


class BookText(QMainWindow, Ui_BookWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('book_window.ui', self)


class ChoiceBook(QMainWindow, Ui_ChoiceBookWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('choice_book_window.ui', self)
        self.text = ""
        self.picture = ""
        self.textButton.clicked.connect(self.change_file_with_text)
        self.pictureButton.clicked.connect(self.change_file_with_picture)

    def change_file_with_text(self):
        self.text = QFileDialog.getOpenFileName(self, "Выберите текстовый файл", "", "Текст (*.txt)")[0]
        self.textEdit.setText(self.text)
        self.update()

    def change_file_with_picture(self):
        types_pictures = "Изображение (*.png);;Изображение (*.jpg);;Изображение (*.jpeg);;Изображение (*.bmp)"
        self.picture = QFileDialog.getOpenFileName(self, "Выберите файл с изображением", "", types_pictures)[0]
        self.pictureEdit.setText(self.picture)
        self.update()

    def initUI(self):
        author = self.authorEdit.text()
        title = self.titleEdit.text()
        year = self.yearEdit.text()
        self.text = self.textEdit.text()
        self.picture = self.pictureEdit.text()
        if not all([author, title, year, self.text]):
            flag = False
            self.statusbar.showMessage("Необходимо заполнить все обязательные поля")
        elif not os.path.isfile(self.text):
            flag = False
            self.statusbar.showMessage("Введите правильное название файла")
        else:
            flag = True
        return flag, author, title, year, self.text, self.picture


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
