import requests
import MySQLdb
import time


setting = {
        "host":"localhost", # Хост для MySQL
        "user":"root", # Логин MySQL
        "passwd":"root", # Пароль MySQL
        "db":"exchanges", # База MySQL
        }

def create_db_and_execute_sql_script():
    try:
        conn = MySQLdb.connect(host=setting['host'], user=setting['user'], passwd=setting['passwd'])
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {setting['db']}")
    except:
        pass
    conn = connectDB()
    cursor = conn.cursor()
    fd = open('./db.sql', 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except Exception as e:
            pass

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
