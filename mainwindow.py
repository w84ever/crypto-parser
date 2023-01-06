from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QHeaderView
from PyQt6 import uic

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)
        self.BinancetableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
