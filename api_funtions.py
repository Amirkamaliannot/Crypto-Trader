# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 17:01:18 2022

@author: Amir
"""

#  MarketData
from kucoin.client import Client
from time import time
import numpy as np

api_key = '61fd42c3fc26a7000117fd0b'
api_secret = '2fed061c-d5ef-4e89-b11a-4de9b4a11445'
api_passphrase = '551Aa8624551Aa8624'


client = Client(api_key, api_secret, api_passphrase)


def live_price(symbol):
    klines = client.get_kline_data(symbol, '1min', start= int(time()- 7200))
    klines = np.array(klines)
    close = klines[: , 2]
    return close
    

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
    client = Client(api_key, api_secret, api_passphrase)
    return client.get_accounts(currency)[0]['available']
    






























