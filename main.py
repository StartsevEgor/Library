import sys
import os
import textwrap

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QTableWidgetItem, QColorDialog, \
    QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from main_window import Ui_MainWindow
from book_window import Ui_BookWindow
from choice_book_window import Ui_ChoiceBookWindow
from library import Library
from random import randint


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        if not os.path.isdir("Libraries"):
            os.mkdir("Libraries")
        self.initUI()

    def initUI(self):
        if not os.path.isfile("settings.txt"):
            self.save_settings("MS Shell Dlg 2", "10", "#000000", "#ffffff")
        else:
            self.apply_settings()
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
        self.searchButton.clicked.connect(self.make_table)
        self.tableWidget.cellDoubleClicked.connect(self.search_if_item_is_clicked)
        self.actionChoose_a_font.triggered.connect(self.change_text_font)
        self.actionChange_size.triggered.connect(self.change_text_size)
        self.actionText_color.triggered.connect(self.change_text_color)
        self.actionBackground_color.triggered.connect(self.change_background_color)

    def change_text_font(self):
        fonts = ("MS Shell Dlg 2", "Arial Narrow", "Century Gothic", "Garamond", "Lucida Sans", "Palatino Linotype",
                 "Segoe UI", "Franklin Gothic Medium", "Book Antiqua", "Cambria", "Rockwell", "Trebuchet MS", "Impact",
                 "Comic Sans MS", "Georgia", "Tahoma", "Calibri", "Times New Roman", "Courier New", "Verdana",
                 "Candara")
        font, ok_pressed = QInputDialog.getItem(self, "Выбор шрифта", "Выберите шрифт", fonts,
                                                fonts.index(self.text_font), True)
        if ok_pressed:
            self.text_font = font
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    def change_text_size(self):
        print(1)
        size, ok_pressed = QInputDialog.getInt(self, "Введите размер", "Какой размер шрифта установить?",
                                               int(self.text_size), 1, 60, 1)
        print(2)
        if ok_pressed:
            self.text_size = str(size)
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color = color.name()
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color = color.name()
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    def save_settings(self, font, size, text_color, background_color):
        print(1, [font, size, text_color, background_color])
        if os.path.isfile("settings.txt"):
            os.remove("settings.txt")
        with open("settings.txt", "w") as settings:
            settings.writelines([font + "\n", size + "\n", text_color + "\n", background_color + "\n"])
        self.text_font, self.text_size, self.text_color, self.background_color = [font, size, text_color,
                                                                                  background_color]

    def apply_settings(self):
        with open("settings.txt", "r") as settings:
            setting_list = list(map(lambda x: x.strip(), settings.readlines()))
            print(5, setting_list)
            self.text_font, self.text_size, self.text_color, self.background_color = setting_list

    def make_table(self, author="", title="", year="", genre=""):
        self.flag2 = True
        if not self.yearEdit.text().isdigit() and self.yearEdit.text():
            self.flag2 = False
            self.statusbar.showMessage('Запишите число в поле "год"')
        else:
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(["Автор", "Название", "Год написания", "Жанр"])
            if not any([author, title, year, genre]):
                data = self.search()
            else:
                data = self.lib.search(author, title, year, genre)
            self.tableWidget.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
                self.color_row(i, QColor(randint(100, 220), randint(100, 220), randint(100, 220)))
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.authorEdit.clear()
            self.titleEdit.clear()
            self.yearEdit.clear()
            self.genreEdit.clear()

    def search_if_item_is_clicked(self, row, col):
        item = self.tableWidget.item(row, col)
        if item.column() == 0:
            self.make_table(item.text())
        elif item.column() == 2:
            self.make_table("", "", item.text())
        elif item.column() == 3:
            self.make_table("", "", "", item.text())
        else:
            self.apply_settings()
            self.book = BookText(self.lib.open_book(item.text()),
                                 [self.text_font, self.text_size, self.text_color, self.background_color])
            print(3, [self.text_font, self.text_size, self.text_color, self.background_color])
            self.book.show()

    def search(self):
        search_by_author = self.authorEdit.text()
        search_by_title = self.titleEdit.text()
        search_by_year = self.yearEdit.text()
        search_by_genre = self.genreEdit.text()
        result = self.lib.search(search_by_author, search_by_title, search_by_year, search_by_genre)
        return result

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

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

    def open_choice_book(self):
        self.choice_book = ChoiceBook()
        self.choice_book.show()
        self.choice_book.add_bookButton.clicked.connect(self.set_data)
        self.choice_book.cancelButton.clicked.connect(self.choice_book.close)

    def set_data(self):
        self.flag, self.author, self.title, self.year, self.genre, self.text, self.picture = self.choice_book.initUI()
        if self.flag:
            self.choice_book.close()
            self.lib.add_book(self.author, self.title, self.year, self.genre, self.text, self.picture)


class BookText(QMainWindow, Ui_BookWindow):
    def __init__(self, text_and_picture, font):
        super().__init__()
        uic.loadUi('book_window.ui', self)
        self.setFixedSize(600, 800)
        self.file_with_text, self.file_with_picture = text_and_picture
        self.picture_flag = True if self.file_with_picture.split("/")[-1] else False
        self.text_font, self.text_size, self.text_color, self.background_color = font
        if self.picture_flag:
            self.initPicture()
        else:
            print(3)
            self.label.deleteLater()
            self.initTextEdit()

    def initPicture(self):
        pixmap = QPixmap(self.file_with_picture)
        self.label.setPixmap(pixmap)

    def initTextEdit(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.textEdit.setReadOnly(True)
        self.textEdit.setFocusPolicy(Qt.NoFocus)
        self.textEdit.installEventFilter(self)

        with open(self.file_with_text, 'r', encoding="utf-8") as file:
            self.text = file.read()
        self.textEdit.setAutoFillBackground(True)
        self.choice_font(self.text_font)
        self.choice_size(self.text_size)
        self.choice_text_color(self.text_color)
        self.choice_background_color(self.background_color)
        self.Choice_font_action.triggered.connect(self.choice_font)
        self.Choice_size_action.triggered.connect(self.choice_size)
        self.Choice_text_color_action.triggered.connect(self.choice_text_color)
        self.Choice_background_color_action.triggered.connect(self.choice_background_color)
        self.initText()

    def initText(self):
        self.textEdit.setText(self.text)

    def keyPressEvent(self, event):
        print(2)
        if self.picture_flag:
            self.picture_flag = False
            self.label.deleteLater()
            self.initTextEdit()

    def choice_font(self, font=None):
        print(4)
        if font:
            self.textEdit.setFontFamily(font.strip())
            self.initText()
        else:
            fonts = ("MS Shell Dlg 2", "Arial Narrow", "Century Gothic", "Garamond", "Lucida Sans", "Palatino Linotype",
                     "Segoe UI", "Franklin Gothic Medium", "Book Antiqua", "Cambria", "Rockwell", "Trebuchet MS",
                     "Impact",
                     "Comic Sans MS", "Georgia", "Tahoma", "Calibri", "Times New Roman", "Courier New", "Verdana",
                     "Candara")
            font, ok_pressed = QInputDialog.getItem(self, "Выбор шрифта", "Выберите шрифт", fonts,
                                                    fonts.index(self.text_font), True)
            if ok_pressed:
                self.textEdit.setFontFamily(font)
                self.initText()
                self.text_font = font

    def choice_size(self, size=None):
        print(5)
        if size:
            self.textEdit.setFontPointSize(int(size.strip()))
            self.initText()
        else:
            print(10)
            size, ok_pressed = QInputDialog.getInt(self, "Введите размер", "Какой размер шрифта установить?",
                                                   int(self.text_size), 1, 60, 1)
            if ok_pressed:
                print(11)
                self.textEdit.setFontPointSize(size)
                self.initText()
                self.text_size = str(size)
                print(12)

    def choice_text_color(self, color=None):
        print(6)
        if color:
            self.textEdit.setTextColor(QColor(color.strip()))
            self.initText()
        else:
            color = QColorDialog.getColor()
            if color.isValid():
                print(1)
                self.textEdit.setTextColor(color)
                self.initText()
                self.text_color = color.name()

    def choice_background_color(self, color=None):
        print(7)
        if color:
            self.textEdit.setStyleSheet(f"background-color: {color.strip()};")
            self.initText()
        else:
            color = QColorDialog.getColor()
            if color.isValid():
                self.textEdit.setStyleSheet(f"background-color: {color.name()};")
                self.initText()
                self.background_color = color.name()

    def closeEvent(self, event):
        if os.path.isfile("settings.txt"):
            os.remove("settings.txt")
        with open("settings.txt", "w") as settings:
            settings.writelines(
                [self.text_font + "\n", self.text_size + "\n", self.text_color + "\n", self.background_color + "\n"])
        event.accept()


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
        genre = self.genreEdit.text()
        self.text = self.textEdit.text()
        self.picture = self.pictureEdit.text()
        if not all([author, title, year, genre, self.text]):
            flag = False
            self.statusbar.showMessage("Необходимо заполнить все обязательные поля")
        elif not os.path.isfile(self.text):
            flag = False
            self.statusbar.showMessage("Введите правильное название файла с текстом")
        elif not year.isdigit():
            flag = False
            self.statusbar.showMessage('Введите число в поле "год"')
        elif self.text.split(".")[-1] != "txt":
            flag = False
            self.statusbar.showMessage("Выберите текстовый файл с расширением .txt")
        elif not os.path.isfile(self.picture) and self.picture != "":
            flag = False
            self.statusbar.showMessage("Введите правильное название файла с обложкой")
        elif self.picture != "" and self.picture.split(".")[-1] not in ["png", "jpg", "jpeg", "bmp"]:
            flag = False
            self.statusbar.showMessage("Выберите файл с обложкой с расширением .png, .jpg, .jpeg или .bmp")
        else:
            flag = True
        return flag, author, title, year, genre, self.text, self.picture


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
