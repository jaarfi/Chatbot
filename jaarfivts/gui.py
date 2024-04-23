#!/usr/bin/python

import sys, os
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox,
                             QApplication, QVBoxLayout,QAbstractItemView,QListWidgetItem )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QListView


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.icon_size = 200
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout(self)

        listWidget = QListWidget()
        #make it icons 
        listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        listWidget.setFlow(QListView.LeftToRight)
        listWidget.setWrapping(True)
        listWidget.setResizeMode(QListView.Adjust)
        listWidget.setMovement(QListView.Snap)
        listWidget.setIconSize(QSize(200,200))

        folder = os.getcwd()
        #folder = "/mnt/Data/pictures/2022-10-30 Sveta Katarina/izbor/1"
        files = os.listdir(folder)
        files = ["A", "B", "C", "D"]

        for foo in files:
            item = QListWidgetItem(foo)
            listWidget.addItem(item)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)
        self.setGeometry(10, 10, 1260, 820)
        self.setWindowTitle('Image renamer')
        self.show()


def main():

    App = QApplication(sys.argv)
    ex = Example()
    sys.exit(App.exec())

if __name__ == '__main__':
    main()