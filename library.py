import os
import shutil

from zipfile import ZipFile


class Library:
    def __init__(self):
        self.name = None

    def make(self):  # Создание пустой библиотеки
        if os.path.isdir("Last library"):
            shutil.rmtree("Last library")
        os.mkdir("Last library")
        open("Last library/database.sqlite", "w").close()
        os.mkdir("Last library/Texts")
        os.mkdir("Last library/Pictures")
        self.name = None
        self.save()

    def open(self, name=None):  # Распаковка библиотеки в отдельную папку
        if name is None:
            with open("last_libraries.txt", "r") as f:
                self.name = f.readlines()[-1][:-1]
                print(self.name)
                ZipFile(self.name, "r").extractall(path="Last library")
        else:
            self.name = name.split("/")[-1]
            ZipFile(self.name, "r").extractall(path="Last library")
        self.save()

    def save(self):
        if self.name is not None:
            name = self.name
        else:
            names = os.listdir("Libraries")
            names = list(filter(lambda x: "Library_" in x, names))
            if not names:
                name = "Libraries/Library_1.lib"
            else:
                name = "Libraries/Library_" + str(max(list(map(lambda x: int(x[:-4].split("_")[1]), names)))) + ".lib"

        archive = ZipFile(name, mode="w")
        archive.write("Last library/Pictures")
        archive.write("Last library/Texts")
        archive.write("Last library/database.sqlite")
        archive.close()

        with open("last_libraries.txt", "r") as f:
            file = f.readlines()
            file = file if not file else file[:-1]
        if name in file:
            file.remove(name)
        os.remove("last_libraries.txt")
        with open("last_libraries.txt", "w") as f:
            f.write(("\n".join(file) + "\n") if file else "")
            f.write(f"{name}\n")
