# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1027, 544)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        MainWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 4, 1, 1)
        self.titleEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleEdit.setObjectName("titleEdit")
        self.gridLayout.addWidget(self.titleEdit, 1, 3, 1, 1)
        self.authorEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.authorEdit.setObjectName("authorEdit")
        self.gridLayout.addWidget(self.authorEdit, 1, 2, 1, 1)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 1, 6, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 6, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 3, 1, 1)
        self.last_actionButton = QtWidgets.QPushButton(self.centralwidget)
        self.last_actionButton.setObjectName("last_actionButton")
        self.gridLayout.addWidget(self.last_actionButton, 0, 0, 1, 1)
        self.next_actionButton = QtWidgets.QPushButton(self.centralwidget)
        self.next_actionButton.setObjectName("next_actionButton")
        self.gridLayout.addWidget(self.next_actionButton, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(False)
        self.label_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 1)
        self.yearEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.yearEdit.setObjectName("yearEdit")
        self.gridLayout.addWidget(self.yearEdit, 1, 4, 1, 1)
        self.genreEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.genreEdit.setObjectName("genreEdit")
        self.gridLayout.addWidget(self.genreEdit, 1, 5, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 5, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_6.addWidget(self.tableWidget)
        self.gridLayout_2.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1027, 25))
        self.menubar.setObjectName("menubar")
        self.File = QtWidgets.QMenu(self.menubar)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.File.setPalette(palette)
        self.File.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.File.setObjectName("File")
        self.Help = QtWidgets.QMenu(self.menubar)
        self.Help.setObjectName("Help")
        self.Main = QtWidgets.QMenu(self.menubar)
        self.Main.setObjectName("Main")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionReference = QtWidgets.QAction(MainWindow)
        self.actionReference.setObjectName("actionReference")
        self.actionChoose_a_font = QtWidgets.QAction(MainWindow)
        self.actionChoose_a_font.setObjectName("actionChoose_a_font")
        self.actionChange_size = QtWidgets.QAction(MainWindow)
        self.actionChange_size.setObjectName("actionChange_size")
        self.actionText_color = QtWidgets.QAction(MainWindow)
        self.actionText_color.setObjectName("actionText_color")
        self.actionOpenLastLibraries = QtWidgets.QAction(MainWindow)
        self.actionOpenLastLibraries.setObjectName("actionOpenLastLibraries")
        self.actionRename = QtWidgets.QAction(MainWindow)
        self.actionRename.setObjectName("actionRename")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionNew_library = QtWidgets.QAction(MainWindow)
        self.actionNew_library.setObjectName("actionNew_library")
        self.actionAdd_book = QtWidgets.QAction(MainWindow)
        self.actionAdd_book.setObjectName("actionAdd_book")
        self.actionBackground_color = QtWidgets.QAction(MainWindow)
        self.actionBackground_color.setObjectName("actionBackground_color")
        self.File.addAction(self.actionNew_library)
        self.File.addSeparator()
        self.File.addAction(self.actionAdd_book)
        self.File.addSeparator()
        self.File.addAction(self.actionOpen)
        self.File.addAction(self.actionOpenLastLibraries)
        self.File.addSeparator()
        self.File.addAction(self.actionSave)
        self.File.addAction(self.actionSave_as)
        self.File.addSeparator()
        self.File.addAction(self.actionRename)
        self.File.addAction(self.actionDelete)
        self.Help.addAction(self.actionReference)
        self.Main.addAction(self.actionChoose_a_font)
        self.Main.addAction(self.actionChange_size)
        self.Main.addAction(self.actionText_color)
        self.Main.addAction(self.actionBackground_color)
        self.menubar.addAction(self.File.menuAction())
        self.menubar.addAction(self.Main.menuAction())
        self.menubar.addAction(self.Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Библиотека"))
        self.label_4.setText(_translate("MainWindow", "Год"))
        self.searchButton.setText(_translate("MainWindow", "Поиск"))
        self.label.setText(_translate("MainWindow", "Поиск по базе данных:"))
        self.pushButton.setText(_translate("MainWindow", "Поиск по тексту"))
        self.label_3.setText(_translate("MainWindow", "Название"))
        self.last_actionButton.setText(_translate("MainWindow", "<"))
        self.next_actionButton.setText(_translate("MainWindow", ">"))
        self.label_2.setText(_translate("MainWindow", "Автор"))
        self.label_5.setText(_translate("MainWindow", "Жанр"))
        self.File.setTitle(_translate("MainWindow", "Файл"))
        self.Help.setTitle(_translate("MainWindow", "Помощь"))
        self.Main.setTitle(_translate("MainWindow", "Главная"))
        self.actionOpen.setText(_translate("MainWindow", "Открыть"))
        self.actionSave.setText(_translate("MainWindow", "Сохранить"))
        self.actionSave_as.setText(_translate("MainWindow", "Сохранить как"))
        self.actionReference.setText(_translate("MainWindow", "Справка"))
        self.actionChoose_a_font.setText(_translate("MainWindow", "Выбрать шрифт"))
        self.actionChange_size.setText(_translate("MainWindow", "Сменить размер"))
        self.actionText_color.setText(_translate("MainWindow", "Цвет текста"))
        self.actionOpenLastLibraries.setText(_translate("MainWindow", "Открыть последние библиотеки"))
        self.actionRename.setText(_translate("MainWindow", "Переименовать"))
        self.actionDelete.setText(_translate("MainWindow", "Удалить"))
        self.actionNew_library.setText(_translate("MainWindow", "Новая библиотека"))
        self.actionAdd_book.setText(_translate("MainWindow", "Добавить книгу"))
        self.actionBackground_color.setText(_translate("MainWindow", "Цвет фона"))
