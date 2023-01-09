from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QTimer
from PyQt6 import QtGui, uic
import threading
from client import client, request_data


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)
        self.BinancetableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.BybittableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.HuobitableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.GatetableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.KucointableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.MexctableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.updateButton.clicked.connect(self.__update_btn_clicked)
        self.ExitButton.clicked.connect(self.__exit_btn_clicked)
        self.updateButton.clicked.connect(self.load_data)

    def __update_btn_clicked(self):
        self.data = {
            'request':'update_from_db',
            'mode':MainWindow.__name__,
        }
        self.update_request = threading.Thread(target=client, args=(self, self.data, ))
        print
        self.update_request.start()
        self.updateButton.setEnabled(False)
        QTimer.singleShot(6000, lambda: self.updateButton.setDisabled(False))

    def load_data(self):

        row1 = 0
        row2 = 0
        row3 = 0
        row4 = 0
        row5 = 0
        row6 = 0

        for token in request_data:
            for binance in token['binance']:
                self.BinancetableWidget.setRowCount(len(token['binance']))
                self.BinancetableWidget.setItem(row1, 0, QTableWidgetItem(binance[0]))
                self.BinancetableWidget.setItem(row1, 1, QTableWidgetItem(binance[1]))
                self.BinancetableWidget.setItem(row1, 2, QTableWidgetItem(binance[2]))
                row1 = row1 + 1
            
            for bybit in token['bybit']:
                self.BybittableWidget.setRowCount(len(token['bybit']))
                self.BybittableWidget.setItem(row2, 0, QTableWidgetItem(bybit[0]))
                self.BybittableWidget.setItem(row2, 1, QTableWidgetItem(bybit[1]))
                self.BybittableWidget.setItem(row2, 2, QTableWidgetItem(bybit[2]))
                row2 = row2 + 1

            for huobi in token['huobi']:
                self.HuobitableWidget.setRowCount(len(token['huobi']))
                self.HuobitableWidget.setItem(row3, 0, QTableWidgetItem(huobi[0]))
                self.HuobitableWidget.setItem(row3, 1, QTableWidgetItem(huobi[1]))
                self.HuobitableWidget.setItem(row3, 2, QTableWidgetItem(huobi[2]))
                row3 = row3 + 1

            for gate in token['gate']:
                self.GatetableWidget.setRowCount(len(token['gate']))
                self.GatetableWidget.setItem(row4, 0, QTableWidgetItem(gate[0]))
                self.GatetableWidget.setItem(row4, 1, QTableWidgetItem(gate[1]))
                self.GatetableWidget.setItem(row4, 2, QTableWidgetItem(gate[2]))
                row4 = row4 + 1

            for kucoin in token['kucoin']:
                self.KucointableWidget.setRowCount(len(token['kucoin']))
                self.KucointableWidget.setItem(row5, 0, QTableWidgetItem(kucoin[0]))
                self.KucointableWidget.setItem(row5, 1, QTableWidgetItem(kucoin[1]))
                self.KucointableWidget.setItem(row5, 2, QTableWidgetItem(kucoin[2]))
                row5 = row5 + 1

            for mexc in token['mexc']:
                self.MexctableWidget.setRowCount(len(token['mexc']))
                self.MexctableWidget.setItem(row6, 0, QTableWidgetItem(mexc[0]))
                self.MexctableWidget.setItem(row6, 1, QTableWidgetItem(mexc[1]))
                self.MexctableWidget.setItem(row6, 2, QTableWidgetItem(mexc[2]))
                row6 = row6 + 1
            
    def __exit_btn_clicked(self):
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        return super().closeEvent(a0)
