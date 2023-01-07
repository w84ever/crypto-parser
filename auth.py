from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6 import uic
from PyQt6 import QtGui
from client import client


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('./ui/login.ui', self)
        self.setFixedSize(350, 450)
        self.pushButton.clicked.connect(self.__login_btn_clicked)
        self.commandLinkButton.clicked.connect(self.__reg_link_btn_clicked)

    def next(self, fun):
        self.__fun = fun

    def next2(self, func):
        self.__func = func

    def __reg_link_btn_clicked(self):
        self.close()
        self.__fun()
        
    def __login_btn_clicked(self):
        if self.usernameLineEdit.text() == '' or self.passwordLineEdit.text() == '':
            print('Заполните все поля!')
        else:
            self.data = {
                'username':self.usernameLineEdit.text(),
                'password':self.passwordLineEdit.text(),
                'mode':Login.__name__
            }
            if client(self, self.data) == 'OK':
                self.close()
                self.__func()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        return super().closeEvent(a0)
        

class Registration(QWidget):

    def __init__(self):
        super(Registration, self).__init__()
        uic.loadUi('./ui/reg.ui', self)
        self.setFixedSize(350, 450)
        self.pushButton.clicked.connect(self.__reg_btn_clicked)

    def next(self, fun):
        self.__fun = fun

    def __reg_btn_clicked(self):
        if self.usernameLineEdit.text() == '' or self.passwordLineEdit.text() == '':
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Ошибка')
            dlg.setText('Введите все поля!')
            button = dlg.exec()
            if button == QMessageBox.StandardButton.Ok:
                print("OK!")
        else:
            self.data = {
                'username':self.usernameLineEdit.text(),
                'password':self.passwordLineEdit.text(),
                'mode':Registration.__name__
            }
            if client(self, self.data) == 'OK':
                self.close()
                self.__fun()
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        return super().closeEvent(a0)
