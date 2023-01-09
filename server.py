import threading
import socket
import json
import pickle
from database import *


def start():

    binance = threading.Thread(target=parse_Binance)
    bybit = threading.Thread(target=parse_Bybit)
    huobi = threading.Thread(target=parse_Huobi)
    gate = threading.Thread(target=parse_Gate)
    kucoin = threading.Thread(target=parse_Kucoin)
    mexc = threading.Thread(target=parse_Mexc)
    request_db = threading.Thread(target=request_to_db)

    binance.start()
    bybit.start()
    huobi.start()
    gate.start()
    kucoin.start()
    mexc.start()
    request_db.start()

def server_listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 6000))
    sock.listen(10)
    print('Server is running, please press Ctrl + C to stop')
    while True:
        global conn, addr
        conn, addr = sock.accept()
        print('connected: ', addr)
        data = conn.recv(1024).decode('UTF-8')
        info_from_user = json.loads(data)
        print(info_from_user)
        if info_from_user['mode'] == 'Login' or 'Registration':
            check_in_db(info_from_user)
        if info_from_user['mode'] == 'MainWindow':
            start()

def check_in_db(info_from_user):
    try:
        connect = connectDB()
        cursor = connect.cursor()
        match info_from_user['mode']:
            case 'Login':
                cursor.execute(f"SELECT username, password FROM users where username like '%{info_from_user['username']}%' AND password like '%{info_from_user['password']}%';")
                result = cursor.fetchall()
                if len(result) > 0:
                    print(result)
                    conn.send(bytes('OK', encoding = 'UTF-8'))
                else:
                    conn.send(bytes('NOK', encoding = 'UTF-8'))
            case 'Registration':
                cursor.execute(f"SELECT username, password FROM users where username like '%{info_from_user['username']}%';")
                result = cursor.fetchall()
                if len(result) == 0:
                    
                    cursor.execute(f"INSERT INTO `users` (`username`, `password`) VALUES ('{info_from_user['username']}', '{info_from_user['password']}');")
                    connect.commit()
                    conn.send(bytes('OK', encoding='UTF-8'))
                else:
                    conn.send(bytes('NOK', encoding='UTF-8'))
    except Exception as e:
        print(e)

def request_to_db():
    exchanges = ['binance', 'bybit', 'huobi', 'gate', 'kucoin', 'mexc']
    data = {}
    for exchange in exchanges:
        connect = connectDB()
        cursor = connect.cursor()
        cursor.execute(f"SELECT symbol, ask, bid FROM {exchange}")
        result = cursor.fetchall()
        data[exchange] = result
    result_to_pickle = pickle.dumps(data)
    conn.send(bytes(result_to_pickle))

if __name__ == '__main__':
    server = threading.Thread(target=server_listen)
    server.start()
