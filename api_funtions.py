# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 17:01:18 2022

@author: Amir
"""

from kucoin.client import Client
from time import time
from time import sleep
import numpy as np
import requests
import pandas as pd

api_key = '61fd42c3fc26a7000117fd0b'
api_secret = '2fed061c-d5ef-4e89-b11a-4de9b4a11445'
api_passphrase = '551Aa8624551Aa8624'


client = Client(api_key, api_secret, api_passphrase)

def live_price(symbol):
    klines = client.get_kline_data(symbol, '1min', start= int(time()- 7200))
    klines = np.array(klines)
    close = klines[: , 2].astype(float)
    close = close[::-1]
    return close


def live_price3(symbol):
    link = "https://api.kucoin.com/api/v1/market/candles?symbol="+symbol+"&type=1min"
    klines = requests.get(link).json()['data']
    klines = np.array(klines)
    close = klines[: , 2].astype(float)
    close = close[::-1]
    return close

        

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
    try:
        client.create_market_order(symbol, 'buy', funds=str(size))#, size='1')
        return True
    
    except :return False


def sell(symbol , size):
    try:
        client.create_market_order(symbol, 'sell', size=str(size))#, size='1')
        return True
    
    except :return False
    
    
    
def currency_Inventory(currency):
    return float(client.get_accounts(currency)[0]['available'])



def usdt_percentage(currency):
    
    link = "https://min-api.cryptocompare.com/data/price?fsym="+currency+"&tsyms=USDT&e=kucoin"
    currency_price = requests.get(link).json()['USDT']
    
    currency_list = client.get_accounts()
    try:
        total_currency = [float(i['available']) for i in currency_list if (i['currency'] == currency)][0]
        total_currency = total_currency * currency_price
    
    except:
    
        total_currency = 0
  
    total_usdt = [float(i['available']) for i in currency_list if (i['currency'] == 'USDT')][0]
    print(total_usdt)
    
    p =(total_usdt / (total_usdt + total_currency))*100
    
    return float("{:.2f}".format(p))



def total_money(price):
    currency_list = client.get_accounts()
    all_ = 0
    for i in currency_list:
        if (i['currency']=='USDT'):
            all_ += float(i['available'])
        else:
            # link = "https://min-api.cryptocompare.com/data/price?fsym="+i['currency']+"&tsyms=USDT&e=kucoin"
            # price = requests.get(link).json()['USDT']
            all_ += price * float(i['available'])
    return float("{:.2f}".format(all_))



def internet_on():
    try:
        requests.get('https://min-api.cryptocompare.com', timeout=5)
        return True
    except: 
        return False
    
# print(total_money())


