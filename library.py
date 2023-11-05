import os
import shutil
import sqlite3

from zipfile import ZipFile, ZIP_DEFLATED


def make_database():
    con = sqlite3.connect("Last library/database.sqlite")
    cur = con.cursor()
    cur.executescript("""CREATE TABLE list_authors (ID INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT);
                CREATE TABLE list_years (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT);
                CREATE TABLE list_genres (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT);
                CREATE TABLE books (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                author INTEGER REFERENCES list_authors (ID),
                title TEXT,
                year INTEGER REFERENCES list_years (ID),
                genre INTEGER REFERENCES list_genres (ID),
                text TEXT,
                picture TEXT);
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

    def open_book(self, title):
        con = sqlite3.connect("Last library/database.sqlite")
        cur = con.cursor()
        result = cur.execute(f'SELECT text, picture FROM books WHERE title = "{title}"').fetchall()[0]
        return ["Last library/Texts/" + result[0], "Last library/Pictures/" + result[1]]

    def search(self, author="", title="", year="", genre=""):
        con = sqlite3.connect("Last library/database.sqlite")
        cur = con.cursor()
        result = list(map(lambda x: "".join(list(x)), cur.execute(f"""SELECT title FROM books WHERE
                author IN (SELECT ID FROM list_authors WHERE author LIKE "%{author}%")
                AND title IN (SELECT title FROM books WHERE title LIKE "%{title}%")
                AND year IN (SELECT ID FROM list_years WHERE year LIKE "%{year}%")
                AND genre IN (SELECT ID FROM list_genres WHERE genre LIKE "%{genre}%")""").fetchall()))
        result = list(map(lambda x: [cur.execute(f'SELECT author FROM list_authors WHERE ID = '
                                                 f'(SELECT author FROM books WHERE title = "{x}")').fetchall()[0][0],
                                     x,
                                     cur.execute(f'SELECT year FROM list_years WHERE ID = '
                                                 f'(SELECT year FROM books WHERE title = "{x}")').fetchall()[0][0],
                                     cur.execute(f'SELECT genre FROM list_genres WHERE ID = '
                                                 f'(SELECT genre FROM books WHERE title = "{x}")').fetchall()[0][0]],
                          result))
        result.sort(key=lambda x: x[1])
        return result

    def add_book(self, author, title, year, genre, text, picture):
        con = sqlite3.connect("Last library/database.sqlite")
        cur = con.cursor()
        cur.execute(f'INSERT INTO list_authors(author) VALUES("{author}")')
        con.commit()
        cur.execute(f'INSERT INTO list_years(year) VALUES("{year}")')
        con.commit()
        cur.execute(f'INSERT INTO list_genres(genre) VALUES("{genre}")')
        con.commit()
        cur.execute(f"""INSERT INTO books(author, title, year, genre, text, picture)
                VALUES((SELECT ID FROM list_authors WHERE author = "{author}"),
                "{title}",
                (SELECT ID FROM list_years WHERE year = "{year}"),
                (SELECT ID FROM list_genres WHERE genre = "{genre}"),
                "{text.split('/')[-1]}",
                "{picture.split('/')[-1]}")""")
        con.commit()
        if text != f"Last library/Texts/{text.split('/')[-1]}":
            shutil.copyfile(text, f"Last library/Texts/{text.split('/')[-1]}")
        if picture and picture != f"Last library/Pictures/{picture.split('/')[-1]}":
            shutil.copyfile(picture, f"Last library/Pictures/{picture.split('/')[-1]}")
        self.save()

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
            with open("last_libraries.txt", "r", encoding="utf-8") as f:
                self.name = f.readlines()[-1].strip()
        shutil.rmtree("Last library")
        os.mkdir("Last library")
        with ZipFile(self.name, "r") as archive:
            archive.extractall(path="Last library")
        self.save()

    def save(self):
        self.name += "\n" if "\n" not in self.name else ""
        archive = ZipFile(self.name.strip(), mode="w")
        archive.write("Last library/database.sqlite", "database.sqlite")
        archive.write("Last library/Pictures", "Pictures")
        archive.write("Last library/Texts", "Texts")
        print(os.listdir("Last library/Pictures"), os.listdir("Last library/Texts"))
        for file in os.listdir("Last library/Pictures"):
            if file:
                archive.write("Last library/Pictures/" + file, "Pictures/" + file)
        for file in os.listdir("Last library/Texts"):
            if file:
                archive.write("Last library/Texts/" + file, "Texts/" + file)
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
