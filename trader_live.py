# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 13:01:27 2022

@author: Amir
"""


import talib as ta
import requests
import pandas as pd
import numpy as np
import time
import csv
import api_funtions as api
from get_log import send_message



currency = 'BTC'

currency_market = 'BTC-USDT'
RSI_PERIOD = 14
trans_ratio = 6/10


last_buy = 'first'
last_sell = 0
b = ''
not_action_step =0
high =65
down =35

with open('history.csv', newline='') as f:
    reader = csv.reader(f)
    history = list(reader)



def connect_to_api(currency, limit=500):
    
        link = "https://min-api.cryptocompare.com/data/v2/histominute?fsym="+currency+"&tsym=usdt&limit="+str(limit)
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
        
        return cl
    
    
def Action_func(type_action):
    
        global last_sell,last_buy, local_min, local_max, total_cash, total_bit, high, down
        
        
        if  (type_action == 'sell' and cl_array[-1] > last_buy):

            
            temp_amount = "{:.2f}".format(float(api.currency_Inventory(currency))*97/100)
            
            is_sell = api.sell(currency_market ,temp_amount )
            
            if (is_sell):
                history.append(['sell',time_str, str("{:.5f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1],last_sell, float(temp_amount)*cl_array[-1] ,int(a[-1])]) 
                print('sell')
                send_message([history[0],history[-1]])
            else: print('ops not sell , wrong ', temp_amount )

            last_sell = cl_array[-1]
            high =65

            
        elif(type_action == 'buy '):
            
            temp_amount = "{:.3f}".format(float(api.currency_Inventory('usdt'))*97/100)
            is_buy = api.buy(currency_market ,temp_amount )
            if (is_buy):
                history.append(['buy ',time_str, str("{:.2f}".format((last_sell- cl_array[-1])/last_sell*100))+'%', cl_array[-1],'------', temp_amount, int(a[-1])]) 
                print('buy')
                send_message([history[0],history[-1]])
            else: print('ops not buy , wrong',  temp_amount )

            last_buy = cl_array[-1]
            down =35

        
        
    
    
def update_locals():
        global local_max ,local_min ,last_buy ,last_sell, action
        
        
        if (last_buy =='first'):
                last_buy = cl_array[-1]
                last_sell = cl_array[-1]
                local_max = cl_array[-1]
                local_min = cl_array[-1]

                    
            
        action = 0

        



def time_now(type_time = 'str'):
    
        if(type_time == 'str'):
            named_tuple = time.localtime()
            time_str = time.strftime("%H:%M:%S", named_tuple) 
            return time_str
    
    

print('\n##START====> '+ time_now())

epoch = 0
while(True):
    # send_message([history[0],history[-1]])
    start = time.time()
    epoch += 1
    print('\n#########==> Epoch : ',epoch ,' ##################################\n')
    

    cl = connect_to_api(currency, limit=250)
    
    cl_array = cl.values
    
    a = np.array(ta.RSI(cl, RSI_PERIOD)) 
    
    time_str = time_now()  
    
    update_locals()

    if(b==''):
        if  (a[-1] >= high):# and all(a[-2:-1] < high)) :
            b= 'up'
            print('up')
            not_action_step =0

        elif(a[-1] <= down):# and all(a[-3:-1]>down)) :
            b= 'down'
            print('down')
            not_action_step =0
        else:
            not_action_step+=1
    
    if(b ==''):
        if last_buy + last_buy*0.0052 <= cl_array[-1]:
            print('+5p')
            not_action_step =0
        
            action = 1
            
        if last_buy - last_buy*0.003 > cl_array[-1]:
            print('-p')
            not_action_step =0
            
            break
            action = 1
            
    if(not_action_step >= 15): 
        high -=1.5
        down +=1.5
        not_action_step -= 10
        
        
        
    if b  ==  'up' and a[-1] >= a[-2]:
        action = 1
        b= ''
    
    if b == 'down' and a[-1] <= a[-2]:
        action = -1
        b= ''
        
        
        
                    
    if(action == 1):
        
        if not (history[-1][0] == 'sell'):
                Action_func('sell')
                
            
    elif(action == -1):  
        
        if not(history[-1][0] == 'buy '): 
                Action_func('buy ')
    
    
    
    
    with open('history.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(history)
        f.close()
    
    print('Time  : ',time_str)
    print('RSI   : ',a[-1])
    print('USDT  : ', "{:.4f}".format(float(api.currency_Inventory('usdt'))))   
    print('Currency: ', "{:.5f}".format(float(api.currency_Inventory(currency))))    
    print('Price : ' , cl_array[-1])        
    print(*history, sep = "\n")
    end = time.time()


    time.sleep(60 - (end-start))
                
            
            
            
            
     
            
            
            
            
            
            
            
            
            
