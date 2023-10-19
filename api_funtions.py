# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 17:01:18 2022

@author: Amir
"""

# from kucoin.client import Client
from time import time
import numpy as np
import requests
import pandas as pd
import share

api_key = ''
api_secret = ''
api_passphrase = ''


# client = Client(api_key, api_secret, api_passphrase)

# def live_price(symbol):
#     klines = client.get_kline_data(symbol, '1min', start= int(time()- 7200))
#     klines = np.array(klines)
#     close = klines[: , 2].astype(float)
#     close = close[::-1]
#     return close
assets = 10000
crypto = 0

currency = share.currency
    
def live_price2(currency, limit=500):
    
        link = "https://min-api.cryptocompare.com/data/v2/histominute?fsym="+currency+"&e=kucoin&tsym=usdt&limit="+str(limit)
        historical_get = requests.get(link)
        historical_json = historical_get.json()
        
        historical_dict = historical_json['Data']
        historical_dict = historical_dict['Data']
    
        df = pd.DataFrame(historical_dict,
                                     columns=['close', 'high', 'low', 'open', 'time', 'volumefrom', 'volumeto'],
                                     dtype='float64')
        
        posix_time = pd.to_datetime(df['time'], unit='s')
        
        df.insert(0, "Date", posix_time) 
        df.drop("time", axis = 1, inplace = True)
        cl = df['close']
        
        return cl.values
    

def buy(symbol , size):
    global assets ,crypto 
    link = "https://min-api.cryptocompare.com/data/price?fsym="+currency+"&tsyms=USDT&e=kucoin"
    price = requests.get(link).json()['USDT']
    crypto = assets / price
    assets = 0

def sell(symbol , size):
    global assets ,crypto 
    link = "https://min-api.cryptocompare.com/data/price?fsym="+currency+"&tsyms=USDT&e=kucoin"
    price = requests.get(link).json()['USDT']
    assets = crypto * price
    crypto = 0
    
    
    
def currency_Inventory(currency):
    global assets ,crypto 
    return crypto 



def usdt_percentage(currency):
    global assets ,crypto 
    link = "https://min-api.cryptocompare.com/data/price?fsym="+currency+"&tsyms=USDT&e=kucoin"
    price = requests.get(link).json()['USDT']
    total = price * crypto + assets
    return assets/total



def total_money():
    global assets ,crypto 
    link = "https://min-api.cryptocompare.com/data/price?fsym="+currency+"&tsyms=USDT&e=kucoin"
    price = requests.get(link).json()['USDT']
    total = price * crypto + assets
    return total



def internet_on():
    try:
        requests.get('https://min-api.cryptocompare.com', timeout=5)
        return True
    except: 
        return False
  
print(total_money())




