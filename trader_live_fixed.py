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
import api_funtions as api

currency = 'luna'
currency_market = 'LUNA-USDT'
RSI_PERIOD = 14
trans_ratio = 6/10

history = [['type','time_hms','Prof', 'Price', 'buy_in', 'Amount', 'RSI' ], ['------------------------------------------------------------']]
last_buy = 'first'
last_sell = 0
local_max = 0
local_min = 0
b = ''
not_action_step =0
high =67
down =35
# high_sell = 70
# down_sell = 30



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
            
            if not all(a[-4:-1] < high) and (last_sell*1.0008 >= cl_array[-1]) and history[-1][0]=='sell':
                print('not now')
                return False
            
            # temp_amount = "{:.3f}".format(float(api.currency_Inventory(currency))*trans_ratio)
            temp_amount = buy_amount
            
            
            is_sell = api.sell(currency_market ,"{:.2f}".format(temp_amount) )
            
            if (is_sell):
                history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1],last_sell, float(temp_amount)*cl_array[-1] ,int(a[-1])]) 
                print('sell')
            else: print('ops not sell , wrong ', "{:.2f}".format(temp_amount) )

            last_sell = cl_array[-1]

            
        elif(type_action == 'buy '):
            if not all(a[-4:-1] > down) and (last_buy*0.9992 <= cl_array[-1]) and history[-1][0]=='buy ':
                print('not now')
                return False
            
            temp_amount = "{:.3f}".format(float(api.currency_Inventory('usdt'))*trans_ratio)
            is_buy = api.buy(currency_market ,temp_amount )
            if (is_buy):
                history.append(['buy ',time_str, str("{:.2f}".format((last_sell- cl_array[-1])/last_sell*100))+'%', cl_array[-1],'------', temp_amount, int(a[-1])]) 
                print('buy')
            else: print('ops not buy , wrong')

            # last_buy = cl_array[-1]


            
        local_min = cl_array[-1]
        local_max = cl_array[-1]
        high =67
        down =35
    
    
def update_locals():
        global local_max ,local_min ,last_buy ,last_sell, action
        
        
        if (last_buy =='first'):
            last_buy = cl_array[-1]
            last_sell = cl_array[-1]
            local_max = cl_array[-1]
            local_min = cl_array[-1]
            
        temp_buy_price = 0
        temp_buy_amount= 0
        for i in history[::-1]:
            if i[0] == 'buy ':
                temp_buy_price+= i[3]* float(i[5])
                temp_buy_amount+= float(i[5])
            else :
                break
        if(temp_buy_price != 0):
            last_buy= temp_buy_price / temp_buy_amount
        temp_buy_amount = temp_buy_amount/cl_array[-1]
            
        
        if (local_max < cl_array[-1]):
            local_max = cl_array[-1]
            
        if (local_min > cl_array[-1]):
            local_min = cl_array[-1]
            
        action = 0
        
        return temp_buy_amount
        



def time_now(type_time = 'str'):
    
        if(type_time == 'str'):
            named_tuple = time.localtime()
            time_str = time.strftime("%H:%M:%S", named_tuple) 
            return time_str
    
    

print('\n##START====> '+ time_now())

epoch = 0
while(True):
    epoch += 1
    print('\n#########==> Epoch : ',epoch ,' ##################################\n')
    

    cl = connect_to_api(currency, limit=250)
    
    cl_array = cl.values
    
    a = np.array(ta.RSI(cl, RSI_PERIOD)) 
    
    time_str = time_now()  
    
    buy_amount = update_locals()

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
        if last_buy + last_buy*0.006 <= cl_array[-1]:
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
        
        if not (history[-1][0] == 'sell'):# and history[-2][0] == 'sell'): 
                Action_func('sell')
                
        # elif(history[-1][3] + history[-1][3]*0.006 <= cl_array[-1]):
        #         Action_func('sell')
            
            
    elif(action == -1):  
        
        if not(history[-1][0] == 'buy ' and history[-2][0] == 'buy '): 

                Action_func('buy ')
                
        elif(history[-1][3] - history[-1][3]*0.004 >= cl_array[-1]):
 
                Action_func('buy ')
    
    print('Time  : ',time_str)
    print('RSI   : ',a[-1])
    print('USDT  : ', "{:.4f}".format(float(api.currency_Inventory('usdt'))))   
    print('Currency: ', "{:.4f}".format(float(api.currency_Inventory(currency))))    
    print('last_buy: ', last_buy)
    print('buy_amount: ', buy_amount)
    print('Price : ' , cl_array[-1])        
    print(*history, sep = "\n")


    time.sleep(58)
                
            
            
            
            
     
            
            
            
            
            
            
            
            
            
