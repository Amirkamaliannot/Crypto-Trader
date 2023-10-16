# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 13:01:27 2022

@author: Amir
"""


import talib as ta
from matplotlib import pyplot as plt

import requests
import pandas as pd
import numpy as np
# link for Bitcoin Data
link = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=link&tsym=usdt&limit=1000"

# API request historical
historical_get = requests.get(link)
# access the content of historical api request
historical_json = historical_get.json()

# extract json data as dictionary
historical_dict = historical_json['Data']
historical_dict = historical_dict['Data']

# extract Final historical df
df = pd.DataFrame(historical_dict,
                             columns=['close', 'high', 'low', 'open', 'time', 'volumefrom', 'volumeto'],
                             dtype='float64')

# time column is converted to "YYYY-mm-dd hh:mm:ss" ("%Y-%m-%d %H:%M:%S")
posix_time = pd.to_datetime(df['time'], unit='s')

# append posix_time
df.insert(0, "Date", posix_time)

# drop unix time stamp
df.drop("time", axis = 1, inplace = True)



# extract OHLC 
op = df['open']
hi = df['high']
lo = df['low']
cl = df['close']
# create columns for each pattern

RSI_PERIOD = 14
a = ta.RSI(cl, RSI_PERIOD)    



b = 0
x = np.zeros((len(a),1))

for i in range(len(x)):
    if (not b):
        
        if a[i] >= 70 and all(a[i-4:i-1]<70) :
            # x[i] = 1
            b = 1
    
    else:
        if a[i] < a[i-1]:
            x[i] = 1
            b= 0
            
for i in range(len(x)):
    if (not b):
        
        if a[i] <= 30 and all(a[i-4:i-1]>30) :
            # x[i] = 1
            b = 1
    
    else:
        if a[i] > a[i-1]:
            x[i] = -1
            b= 0
        
        

plt.subplot(2,1,1)
plt.plot(a)
plt.plot(np.ones((len(a),1))*70)
plt.plot((x*50)+50)
plt.plot(np.ones((len(a),1))*30)
plt.subplot(2,1,2)
plt.plot(cl)
plt.show()

























