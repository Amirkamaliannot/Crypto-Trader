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

link = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=usdt&limit=500"
RSI_PERIOD = 14

history = [['type','time_hms','Prof', ' Price', 'RSI'], ['--------------------------------------------']]
last_buy = 'first'
last_sell = 0
local_max = 0
local_min = 0
b = ''
total_cash = 100000
total_bit = 10
not_action_step =0
high =60
down =40


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
        
        
        if  (type_action == 'sell'):
            if not all(a[-4:-1] < high) and (last_sell*1.0008 >= cl_array[-1]) and history[-1][0]=='sell':
                print('not now')
                return False
                
            history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1], a[-1]]) 
            # history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1], a[-1]]) 
            last_sell = cl_array[-1]
            total_cash +=  cl_array[-1]
            total_bit -= 1
            print('sell')  
            
        elif(type_action == 'buy '):
            if not all(a[-4:-1] > down) and (last_buy*0.9992 <= cl_array[-1]) and history[-1][0]=='buy ':
                print('not now')
                return False
            
            history.append(['buy ',time_str, str("{:.2f}".format((last_sell- cl_array[-1])/last_sell*100))+'%', cl_array[-1], a[-1]]) 
            # history.append(['buy ',time_str, str("{:.2f}".format((last_sell- cl_array[-1])/last_sell*100))+'%', cl_array[-1], a[-1]]) 
            last_buy = cl_array[-1]
            total_cash -=  cl_array[-1]
            total_bit += 1
            print('buy ')  
            
        local_min = cl_array[-1]
        local_max = cl_array[-1]
        high =60
        down =40
    
    
def update_locals():
        global local_max ,local_min ,last_buy ,last_sell, action
        
        if (last_buy =='first'):
            last_buy = cl_array[-1]
            last_sell = cl_array[-1]
            local_max = cl_array[-1]
            local_min = cl_array[-1]
        
        if (local_max < cl_array[-1]):
            local_max = cl_array[-1]
            
        if (local_min > cl_array[-1]):
            local_min = cl_array[-1]
            
        action = 0


def time_now(type_time = 'str'):
    
        if(type_time == 'str'):
            named_tuple = time.localtime()
            time_str = time.strftime("%H:%M:%S", named_tuple) 
            return time_str
    
    
def allow_action(type_action):
    
        if(type_action == 'sell'):
            if(not (history[-1][0] == 'sell' and history[-2][0] == 'sell') or local_min + local_min*0.005 <= cl_array[-1]):    
                return True
            else: return False
            
        if(type_action == 'buy '):
            if(not (history[-1][0] == 'buy ' and history[-2][0] == 'buy ') or local_max - local_max*0.005 >= cl_array[-1]):    
                return True
            else: return False
    

print('##START====> '+ time_now())

epoch = 0
while(True):
    epoch += 1
    print('\n==>Epoch : ',epoch ,' #####################################################\n')
    

    cl = connect_to_api('btc', limit=250)
    
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
        if local_min + local_min*0.005 <= cl_array[-1]:
            print('+5p')
            not_action_step =0
            action = 1
        if local_max - local_max*0.005 >= cl_array[-1]:
            print('-5p')
            not_action_step =0
            action = -1
    
    
    if(not_action_step >= 20): 
        high -=2
        down +=2
        not_action_step -= 10
        
        
    if b =='up' :#and a[-1] > a[-2]:
        action = 1
        b= ''
    
    if b =='down' :# and a[-1] < a[-2]:
        action = -1
        b= ''
        
        
                    
    if(action == 1):
        
        if not (history[-1][0] == 'sell' and history[-2][0] == 'sell'): 
           # if( cl_array[-1] > last_buy and cl_array[-1] > history[-1][2]):
                
                # history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1], a[-1]])  
                # last_sell = cl_array[-1]
                # total_cash +=  cl_array[-1]
                # total_bit -= 1
                # print('sell')  
                Action_func('sell')
                
        elif(last_buy + last_buy*0.004 <= cl_array[-1]):
                # history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1], a[-1]])  
                # last_sell = cl_array[-1]
                # total_cash +=  cl_array[-1]
                # total_bit -= 1
                # print('sell')  
                Action_func('sell')
            
            
    elif(action == -1):  
        
        if not(history[-1][0] == 'buy ' and history[-2][0] == 'buy '): 
           # if( cl_array[-1] < last_sell and cl_array[-1] < history[-1][2]):
                
                # history.append(['buy ', time_str, str("{:.2f}".format((last_sell- cl_array[-1])/last_sell*100))+'%', cl_array[-1], a[-1]]) 
                # last_buy = cl_array[-1]
                # total_cash -=  cl_array[-1]
                # total_bit += 1
                # print('buy ')  
                Action_func('buy ')
                
        elif(last_sell - last_sell*0.004 >= cl_array[-1]):
                # history.append(['sell',time_str, str("{:.2f}".format((last_sell- cl_array[-1])/last_sell*100))+'%', cl_array[-1], a[-1]])  
                # last_sell = cl_array[-1]
                # total_cash +=  cl_array[-1]
                # total_bit -= 1
                # print('sell')  
                Action_func('buy ')
    
    print('Time : ',time_str)
    print('RSI : ',a[-1])
    print('Toltal : ' , total_cash+(total_bit*cl_array[-1]))        
    print('Price : ' , cl_array[-1])        
    print(*history, sep = "\n")


    time.sleep(59)
                
            
            
            
            
     
            
            
            
            
            
            
            
            
            