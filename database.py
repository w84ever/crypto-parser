import requests
import MySQLdb
import time
import threading
import socket
import json

setting = {
        "refreshTime":60, # Время повторной загрузки в секундах
        "host":"localhost", # Хост для MySQL
        "user":"root", # Логин MySQL
        "passwd":"root", # Пароль MySQL
        "db":"exchanges", # База MySQL
        }

def connectDB():
    return MySQLdb.connect(host=setting['host'], user=setting['user'], passwd=setting['passwd'], db=setting['db'])

def save_parse(price, exchange):
    conn = connectDB()
    cursor = conn.cursor()
    for symbol in price:
        cursor.execute(f"INSERT INTO `{exchange}` (`symbol`, `ask`, `bid`) VALUES ('{symbol[0]}', '{symbol[1]}', '{symbol[2]}') ON DUPLICATE KEY UPDATE ask = {symbol[1]}, bid = {symbol[2]}, date = CURRENT_TIMESTAMP;") #Check update key
    conn.commit()
    conn.close()

def parse_Binance():
    exchange = 'Binance'
    parse_list = requests.get("https://api.binance.com/api/v3/ticker/24hr").json()
    if 'code' in parse_list:
        print(f"Error code {parse_list['code']} msg = {parse_list['msg']}")
        time.sleep(10)
        return False
    price = []
    for symbol in parse_list:
        try:
            if float(symbol['lastPrice']) > 0:
                price.append([symbol['symbol'], symbol['askPrice'], symbol['bidPrice']])       
        except Exception as e:
            print(e)
    save_parse(price, exchange)

def parse_Bybit():
    exchange = 'Bybit'
    parse_list = requests.get('https://api.bybit.com/spot/quote/v1/ticker/24hr').json()
    if 'code' in parse_list:
        print(f"Error code {parse_list['code']} msg = {parse_list['msg']}")
        time.sleep(10)
        return False
    price = []  
    for symbol in parse_list['result']:
        try:
            if float(symbol['lastPrice']) > 0:
                price.append([symbol['symbol'], symbol['bestAskPrice'], symbol['bestBidPrice']])
        except Exception as e:
            print(e)
    save_parse(price, exchange)

def parse_Huobi():
    exchange = 'Huobi'
    parse_list = requests.get('https://api.huobi.pro/market/tickers').json()
    price = []
    for symbol in parse_list['data']:
        try:
            if float(symbol['low']) > 0:
                price.append([symbol['symbol'], symbol['ask'], symbol['bid']])
        except Exception as e:
            print(e)
    save_parse(price, exchange)

def parse_Gate():
    exchange = 'Gate'
    parse_list = requests.get('https://api.gateio.ws/api/v4/spot/tickers/').json()
    price = []
    for symbol in parse_list:
        try:
            if len(symbol['lowest_ask']) > 0 and len(symbol['highest_bid']) > 0:
                if float(symbol['lowest_ask']) > 0:
                    price.append([symbol['currency_pair'], symbol['lowest_ask'], symbol['highest_bid']])
        except Exception as e:
            print(e)
    save_parse(price, exchange)

def parse_Kucoin():
    exchange = 'Kucoin'
    parse_list = requests.get('https://api.kucoin.com/api/v1/market/allTickers').json()
    price = []
    for symbol in parse_list['data']['ticker']:
        try:
            if float(symbol['last']) > 0:
                price.append([symbol['symbol'], symbol['sell'], symbol['buy']])
        except Exception as e:
            print(e)
    save_parse(price, exchange)

def parse_Mexc():
    exchange = 'Mexc'
    parse_list = requests.get('https://api.mexc.com/api/v3/ticker/24hr').json()
    price = []
    for symbol in parse_list:
        try:
            if float(symbol['lastPrice']) > 0:
                price.append([symbol['symbol'], symbol['askPrice'], symbol['bidPrice']])
        except Exception as e:
            print(e)
    save_parse(price, exchange)

def start():

    binance = threading.Thread(target=parse_Binance)
    bybit = threading.Thread(target=parse_Bybit)
    huobi = threading.Thread(target=parse_Huobi)
    gate = threading.Thread(target=parse_Gate)
    kucoin = threading.Thread(target=parse_Kucoin)
    mexc = threading.Thread(target=parse_Mexc)
    request_db = threading.Thread(target=request_to_db)
    server = threading.Thread(target=server_listen)

    binance.start()
    bybit.start()
    huobi.start()
    gate.start()
    kucoin.start()
    mexc.start()
    server.start()
    # request_db.start()

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
            request_to_db()

def check_in_db(info_from_user):
    try:
        connect = connectDB()
        cursor = connect.cursor()
        match info_from_user['mode']:
            case 'Login':
                cursor.execute(f"SELECT username, password FROM users where username like '%{info_from_user['username']}%' AND password like '%{info_from_user['password']}%';")
                result = cursor.fetchall()
                if len(result) > 0:
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
    connect = connectDB()
    cursor = connect.cursor()
    for exchange in exchanges:
        cursor.execute(f"SELECT symbol, ask, bid FROM {exchange}")
        result = cursor.fetchall()
        result_to_json = json.dumps(result)
        conn.send(bytes(f'{result_to_json}', encoding='UTF-8'))
        
        
if __name__ == '__main__':
    start()
