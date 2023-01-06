from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6 import QtGui
import socket
import json


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('./ui/login.ui', self)
        self.setFixedSize(350, 450)
        self.pushButton.clicked.connect(self.__login_btn_clicked)
        self.commandLinkButton.clicked.connect(self.__reg_link_btn_clicked)
        self.pushButton.setEnabled(False)

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
            client(self, Login.__name__) 

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        return super().closeEvent(a0)
        

class Registration(QWidget):
    def __init__(self):
        super(Registration, self).__init__()
        uic.loadUi('./ui/reg.ui', self)
        self.setFixedSize(350, 450)
        self.pushButton.clicked.connect(self.__reg_btn_clicked)
    
    def __reg_btn_clicked(self):
        if self.usernameLineEdit.text() == '' or self.passwordLineEdit.text() == '':
            print('Заполните все поля!')
        else:
            client(self, Registration.__name__) 


def client(self, cls):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 6000))
    data = {
        'username':self.usernameLineEdit.text(),
        'password':self.passwordLineEdit.text(),
        'mode':cls
    }
    data_to_json = json.dumps(data)
    sock.send(bytes(f'{data_to_json}', encoding = 'UTF-8'))
    ans = sock.recv(1024).decode('UTF-8')
    match data['mode']:
        case 'Login':
            if ans == 'OK':
                print('Верно')
            elif ans == 'NOK':
                print('Неверно!')

        case 'Registration':
            if ans == 'Регистрация прошла успешно!':
                print('Получилось зарегистрироваться!')
            elif ans == 'Такой логин уже есть, введите новый':
                print('Не получилось зарегистрироваться!')
