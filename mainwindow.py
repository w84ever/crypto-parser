from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QHeaderView
from PyQt6 import uic
from auth import client


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)
        self.BinancetableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pushButton.clicked.connect(self.__update_btn_clicked)

    def __update_btn_clicked(self):
        self.data = {
            'request':'update_from_db',
            'mode':MainWindow.__name__
        }
        client(self, self.data)
        




