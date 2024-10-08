import sys
import os

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QTableWidgetItem, QColorDialog, \
    QMessageBox
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

    # Установка стандартного стиля шрифта, создание библиотеки при первом открытии или открытие уже имеющихся стилей
    # и библиотек при последующих; инициализация кнопок интерфейса
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
        self.search_history = []
        self.history_cursor = 0
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
        self.last_actionButton.clicked.connect(self.work_with_search_history)
        self.next_actionButton.clicked.connect(self.work_with_search_history)
        self.actionReference.triggered.connect(self.reference)
        self.make_table()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.make_table()

    # Метод открывает справку
    def reference(self):
        with open("help.txt", "r", encoding="utf-8") as f:
            QMessageBox.question(self, 'Справка', f.read())

    # Метод описывает работу кнопок, отвечающих за за предыдущие и следующие фильтры поиска
    def work_with_search_history(self):
        button_text = self.sender().text()
        button_action = -1 if button_text == "<" else 1
        if -(len(self.search_history)) <= (self.history_cursor + button_action) < 0:
            self.history_cursor += button_action
            author, title, year, genre = self.search_history[self.history_cursor]
            self.make_table(author, title, year, genre)
            self.authorEdit.setText(author)
            self.titleEdit.setText(title)
            self.yearEdit.setText(year)
            self.genreEdit.setText(genre)

    # Метод меняет шрифт книги
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

    # Метод меняет размер текста книги
    def change_text_size(self):
        size, ok_pressed = QInputDialog.getInt(self, "Введите размер", "Какой размер шрифта установить?",
                                               int(self.text_size), 1, 60, 1)
        if ok_pressed:
            self.text_size = str(size)
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    # Метод меняет цвет текста книги
    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color = color.name()
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    # Метод меняет фон книги
    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color = color.name()
            self.save_settings(self.text_font, self.text_size, self.text_color, self.background_color)

    # Метод сохраняет настройки стиля книги
    def save_settings(self, font, size, text_color, background_color):
        if os.path.isfile("settings.txt"):
            os.remove("settings.txt")
        with open("settings.txt", "w") as settings:
            settings.writelines([font + "\n", size + "\n", text_color + "\n", background_color + "\n"])
        self.text_font, self.text_size, self.text_color, self.background_color = [font, size, text_color,
                                                                                  background_color]

    # Метод применяет предыдущие настройки стиля книги
    def apply_settings(self):
        with open("settings.txt", "r") as settings:
            setting_list = list(map(lambda x: x.strip(), settings.readlines()))
            self.text_font, self.text_size, self.text_color, self.background_color = setting_list

    # Метод создаёт таблицу
    def make_table(self, author="", title="", year="", genre=""):
        if not self.yearEdit.text().isdigit() and self.yearEdit.text():
            self.statusbar.showMessage('Запишите число в поле "год"')
        else:
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(["Автор", "Название", "Год написания", "Жанр", "Удалить"])
            if not any([author, title, year, genre]):
                data = self.search()
            else:
                data = self.lib.search(author, title, year, genre)
            self.tableWidget.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
                self.tableWidget.setItem(i, 4, QTableWidgetItem("🗑"))
                self.color_row(i, QColor(randint(100, 220), randint(100, 220), randint(100, 220)))
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.authorEdit.clear()
            self.titleEdit.clear()
            self.yearEdit.clear()
            self.genreEdit.clear()

    # Метод выполняет работу с ячейками таблицы
    def search_if_item_is_clicked(self, row, col):
        item = self.tableWidget.item(row, col)
        if item.column() == 0:
            self.make_table(author=item.text())
        elif item.column() == 2:
            self.make_table(year=item.text())
        elif item.column() == 3:
            self.make_table(genre=item.text())
        elif item.column() == 4:
            title = self.tableWidget.item(row, 1).text()
            valid = QMessageBox.question(
                self, '', "Действительно удалить книгу?", QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.lib.remove_book(title)
                self.make_table()
        else:
            self.apply_settings()
            self.book = BookText(item.text(), self.lib.open_book(item.text()),
                                 [self.text_font, self.text_size, self.text_color, self.background_color])
            self.book.show()

    # Метод ищет книги по фильтрам
    def search(self):
        search_by_author = self.authorEdit.text()
        search_by_title = self.titleEdit.text()
        search_by_year = self.yearEdit.text()
        search_by_genre = self.genreEdit.text()
        if any([search_by_author, search_by_title, search_by_year, search_by_genre]):
            self.search_history.append([search_by_author, search_by_title, search_by_year, search_by_genre])
            self.history_cursor = -1
        result = self.lib.search(search_by_author, search_by_title, search_by_year, search_by_genre)
        return result

    # Метод делает строки таблицы разноцветными
    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    # Метод удаляет библиотеку, а затем открывает предыдущую, если она есть. Если нет, то создаёт новую.
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
            self.lib.make()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")

    # Метод позволяет переименовать библиотеку
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

    # Метод сохраняет файл библиотеки в нужную папку
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

    # Метод создаёт новую библиотеку
    def new_library(self):
        self.lib.save()
        self.lib = Library()
        self.lib.make()
        self.setWindowTitle(f"Библиотека - {self.lib.name}")
        self.make_table()

    # Метод открывает библиотеку из конкретной папки
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
        self.make_table()

    # Метод позволяет открыть библиотеку из списка последних
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
        self.make_table()

    # Метод открывает класс, ответственный за интерфейс добавления книги
    def open_choice_book(self):
        self.choice_book = ChoiceBook()
        self.choice_book.show()
        self.choice_book.add_bookButton.clicked.connect(self.set_data)
        self.choice_book.cancelButton.clicked.connect(self.choice_book.close)

    # Метод сохраняет новую книгу
    def set_data(self):
        self.flag, self.author, self.title, self.year, self.genre, self.text, self.picture = self.choice_book.initUI()
        if self.flag:
            self.choice_book.close()
            self.lib.add_book(self.author, self.title, self.year, self.genre, self.text, self.picture)
            self.make_table(self.author, self.title, self.year, self.genre)


# Класс, ответственный за открытие текста книги с обложкой
class BookText(QMainWindow, Ui_BookWindow):
    def __init__(self, title, text_and_picture, font):
        super().__init__()
        uic.loadUi('book_window.ui', self)
        self.setFixedSize(600, 800)
        self.setWindowTitle(title)
        self.file_with_text, self.file_with_picture = text_and_picture
        self.picture_flag = True if self.file_with_picture.split("/")[-1] else False
        self.text_font, self.text_size, self.text_color, self.background_color = font
        if self.picture_flag:
            self.initPicture()
        else:
            self.label.deleteLater()
            self.initTextEdit()

    # Метод открывает обложку книги
    def initPicture(self):
        pixmap = QPixmap(self.file_with_picture)
        scaled_pixmap = pixmap.scaled(600, 750, Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)
        self.statusbar.showMessage("Нажмите на любую клавишу, чтобы начать чтение")

    # Метод открывает текст книги и инициализирует кнопки интерфейса
    def initTextEdit(self):
        self.statusbar.showMessage("")
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

    # Метод добавляет текст в поле textEdit
    def initText(self):
        self.textEdit.setText(self.text)

    # Метод закрывает картинку обложки при нажатии на любую клавишу
    def keyPressEvent(self, event):
        if self.picture_flag:
            self.picture_flag = False
            self.label.deleteLater()
            self.initTextEdit()

    # Метод меняет шрифт книги
    def choice_font(self, font=None):
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

    # Метод меняет размер текста книги
    def choice_size(self, size=None):
        if size:
            self.textEdit.setFontPointSize(int(size.strip()))
            self.initText()
        else:
            size, ok_pressed = QInputDialog.getInt(self, "Введите размер", "Какой размер шрифта установить?",
                                                   int(self.text_size), 1, 60, 1)
            if ok_pressed:
                self.textEdit.setFontPointSize(size)
                self.initText()
                self.text_size = str(size)

    # Метод меняет цвет текста книги
    def choice_text_color(self, color=None):
        if color:
            self.textEdit.setTextColor(QColor(color.strip()))
            self.initText()
        else:
            color = QColorDialog.getColor()
            if color.isValid():
                self.textEdit.setTextColor(color)
                self.initText()
                self.text_color = color.name()

    # Метод меняет цвет фона книги
    def choice_background_color(self, color=None):
        if color:
            self.textEdit.setStyleSheet(f"background-color: {color.strip()};")
            self.initText()
        else:
            color = QColorDialog.getColor()
            if color.isValid():
                self.textEdit.setStyleSheet(f"background-color: {color.name()};")
                self.initText()
                self.background_color = color.name()

    # Метод сохраняет настройки стиля книги при её закрытии
    def closeEvent(self, event):
        if os.path.isfile("settings.txt"):
            os.remove("settings.txt")
        with open("settings.txt", "w") as settings:
            settings.writelines(
                [self.text_font + "\n", self.text_size + "\n", self.text_color + "\n", self.background_color + "\n"])
        event.accept()


# Класс, ответственный за окно добавления книги
class ChoiceBook(QMainWindow, Ui_ChoiceBookWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('choice_book_window.ui', self)
        self.text = ""
        self.picture = ""
        self.textButton.clicked.connect(self.change_file_with_text)
        self.pictureButton.clicked.connect(self.change_file_with_picture)

    # Метод отвечает за выбор файла текста книги
    def change_file_with_text(self):
        self.text = QFileDialog.getOpenFileName(self, "Выберите текстовый файл", "", "Текст (*.txt)")[0]
        self.textEdit.setText(self.text)
        self.update()

    # Метод отвечает за выбор файла обложки книги
    def change_file_with_picture(self):
        types_pictures = "Изображение (*.png);;Изображение (*.jpg);;Изображение (*.jpeg);;Изображение (*.bmp)"
        self.picture = QFileDialog.getOpenFileName(self, "Выберите файл с изображением", "", types_pictures)[0]
        self.pictureEdit.setText(self.picture)
        self.update()

    # Метод, отвечающий за сохранение информации о новой книге и проверку на ошибки при вводе
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
