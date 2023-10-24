import os

from zipfile import ZipFile


class Library:
    def __init__(self, name=None):
        if name is None:
            if not os.path.isdir("Last library"):
                if os.path.isfile("last_libraries.txt"):
                    self.last_libraries = open("last_libraries.txt",
                                               "r").readlines()  # список последних открытых библиотек
                    self.last_library = self.last_libraries[-1][:-1]

                    os.mkdir("Last library")
                    os.rename(self.last_library, self.last_library[:-3] + "zip")
                    self.last_library = "Libraries/" + self.last_library[:-3] + "zip"

                    # Распаковка последней библиотеки в отдельную папку для более комфортной работы с ней
                    ZipFile(self.last_library, "r").extractall(path="Last library")
                else:
                    self.last_libraries = open("last_libraries.txt", "w")
                    self.last_libraries.write("Library.lib\n")

    def new_library(self, name):
        name = ("Library_" + name) if name.isdigit() else name
        database = open("Libraries/")
