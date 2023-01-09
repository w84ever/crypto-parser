import socket
import json
import pickle
from PyQt6.QtWidgets import QMessageBox

request_data = []

def client(self, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 6000))
    data_to_json = json.dumps(data)
    sock.send(bytes(f'{data_to_json}', encoding = 'UTF-8'))
    if data['mode'] != 'MainWindow':
        ans = sock.recv(1024).decode('UTF-8')
    match data['mode']:
        case 'Login':
            if ans == 'OK':
                print('Можете войти')
            elif ans == 'NOK':
                # print('Неправильный логин или пароль!')
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Ошибка')
                dlg.setText('Неправильный логин или пароль!')
                button = dlg.exec()
                if button == QMessageBox.StandardButton.Ok:
                    print("OK!")
        case 'Registration':
            if ans == 'OK':
                print('Получилось зарегистрироваться!')
            elif ans == 'NOK':
                print('Такой логин уже есть, введите новый!')
        case 'MainWindow':
            data = b''
            while True:
                packet = sock.recv(4096)
                data += packet
                if not packet: break
            ans = pickle.loads(data)
            request_data.clear()
            request_data.append(ans)
    return ans
