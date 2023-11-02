import os
import shutil
import sqlite3

from zipfile import ZipFile


def make_database():
    con = sqlite3.connect("Last library/database.sqlite")
    cur = con.cursor()
    cur.executescript("""CREATE TABLE list_authors (ID INTEGER PRIMARY KEY AUTOINCREMENT, year TEXT);
                CREATE TABLE list_years (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT);
                CREATE TABLE list_genres (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT);
                CREATE TABLE books (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                author INTEGER REFERENCES list_authors (ID),
                title TEXT,
                year INTEGER REFERENCES list_years (ID),
                genre INTEGER REFERENCES list_genres (ID),
                file_with_text TEXT,
                file_with_picture TEXT);
                """)


class Library:
    def __init__(self, name=None, flag_new_file=True):
        self.name = name
        if (self.name is None) and flag_new_file:
            names = os.listdir("Libraries")
            names = list(filter(lambda x: "Library_" in x, names))
            if not names:
                self.name = "Libraries/Library_1.lib"
            else:
                self.name = "Libraries/Library_" + str(
                    max(list(map(lambda x: int(x[:-4].split("_")[1]) + 1, names)))) + ".lib"

    # def search(self, author, title, year, genre):

    def make(self):  # Создание пустой библиотеки
        if os.path.isdir("Last library"):
            shutil.rmtree("Last library")
        os.mkdir("Last library")
        open("Last library/database.sqlite", "w").close()
        make_database()
        os.mkdir("Last library/Texts")
        os.mkdir("Last library/Pictures")
        self.save()

    def open(self):  # Распаковка библиотеки в отдельную папку
        if self.name is None:
            with open("last_libraries.txt", "r") as f:
                self.name = f.readlines()[-1].strip()
        shutil.rmtree("Last library")
        os.mkdir("Last library")
        with ZipFile(self.name, "r") as archive:
            archive.extractall(path="Last library")
        self.save()

    def save(self):
        self.name += "\n" if "\n" not in self.name else ""
        archive = ZipFile(self.name.strip(), mode="w")
        archive.write("Last library/Pictures", "Pictures")
        archive.write("Last library/Texts", "Texts")
        archive.write("Last library/database.sqlite", "database.sqlite")
        archive.close()
        with open("last_libraries.txt", "r") as f:
            file = f.readlines()
            file = file if file else []
        if self.name in file:
            file.remove(self.name)
        os.remove("last_libraries.txt")
        file.append(self.name)
        with open("last_libraries.txt", "w") as f:
            f.writelines(file)
