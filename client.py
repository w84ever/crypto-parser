import socket
import json


def client(self, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 6000))
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
            if ans == 'OK':
                print('Получилось зарегистрироваться!')
            elif ans == 'NOK':
                print('Не получилось зарегистрироваться!')
        case 'MainWindow':
            print(ans)
    return ans