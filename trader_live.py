# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 13:01:27 2022

@author: Amir
"""


import talib as ta
import numpy as np
import time
import csv
import os.path
import api_funtions as api
from get_log import send_message




currency = 'ADA'
RSI_PERIOD = 14
# trans_ratio = 6/10
high =63
down =37
sl_ratio = 0.3 






    
def sell_and_stop():
    global last_buy , last_sell, history , time_str, cl_array
    
    temp_amount = "{:.3f}".format(float(api.currency_Inventory(currency))*99/100)
    is_sell = api.sell(currency_market ,temp_amount )
    if (is_sell):
        history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1],last_sell, float(temp_amount)*cl_array[-1] ,int(a[-1]), api.total_money()]) 
        print('limit')
        last_sell = cl_array[-1]
    else: 
        print('god fme !!!! doesn,t sell , do something')
        exit()
        
    temp_price = cl_array[-1]
    time.sleep(60)
    cl_array = api.live_price2(currency, limit=1)
    
    if (temp_price  > cl_array[-1]):
        print('waiting')
        time.sleep(60)
        
        cl_array = api.live_price2(currency, limit=1)
        temp_price = cl_array[-1]
        if (temp_price  > cl_array[-1]):
            print('waiting')
            temp_price = cl_array[-1]
            time.sleep(60)
            
            cl_array = api.live_price2(currency, limit=1)
            if (temp_price  > cl_array[-1]):
                print('waiting')
                temp_price = cl_array[-1]
                time.sleep(60)
                
                cl_array = api.live_price2(currency, limit=1)
                if (temp_price  > cl_array[-1]):
                    print('waiting')
                    temp_price = cl_array[-1]
                    time.sleep(90)
                    
                    cl_array = api.live_price2(currency, limit=1)
                    if (temp_price  > cl_array[-1]):
                        print('waiting')
                        temp_price = cl_array[-1]
                        time.sleep(120)
                        
                        cl_array = api.live_price2(currency, limit=1)
                        if (temp_price  > cl_array[-1]):
                            print('waiting')
                            temp_price = cl_array[-1]
                            time.sleep(300)
                            
                            cl_array = api.live_price2(currency, limit=1)
                            if (temp_price > cl_array[-1]):
                                print('stop')
                                exit()
                        
    time_str = time_now()                  
    temp_amount = "{:.3f}".format(float(api.currency_Inventory('USDT'))*99/100)
    is_buy = api.buy(currency_market ,temp_amount )
    if (is_buy):
        history.append(['buy ',time_str, '-----', cl_array[-1],'------', temp_amount, int(a[-1]), api.total_money()]) 
        print('limit')
        last_buy = cl_array[-1]
    else: 
        print('god fme !!!! doesn,t sell , do something')
        exit()
    
        
    
    
def Action_func(type_action):
    
        global last_sell,last_buy, local_min, local_max, total_cash, total_bit, high, down, turn
        
        
        if  (type_action == 'sell'):

            
            temp_amount = "{:.2f}".format(float(api.currency_Inventory(currency))*99/100)
            
            is_sell = api.sell(currency_market ,temp_amount )
            if (is_sell):
                history.append(['sell',time_str, str("{:.3f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1],last_sell, "{:.2f}".format(temp_amount)*cl_array[-1] ,int(a[-1]) ,api.total_money()]) 
                print('sell')
                turn = 'buy'
                send_message([history[0],history[-1]])
                
            else: print('ops not sell , wrong ', temp_amount )

            last_sell = cl_array[-1]
            high =63

            
        elif(type_action == 'buy '):
            
            temp_amount = "{:.2f}".format(float(api.currency_Inventory('usdt'))*99/100)
            
            is_buy = api.buy(currency_market ,temp_amount )
            if (is_buy):
                history.append(['buy ',time_str, '-----', cl_array[-1],'------', "{:.2f}".format(temp_amount), int(a[-1]) ,api.total_money()]) 
                print('buy')
                turn = 'sell'
                send_message([history[0],history[-1]])
            else: print('ops not buy , wrong',  temp_amount )

            last_buy = cl_array[-1]
            down =37

        
def update_locals():
        global last_buy ,last_sell, action
        
        
        if (last_buy =='first'):
            # if(len(history)==2):
                last_buy = cl_array[-1]
                last_sell = cl_array[-1]
            
            # else:
            #     if(history[-1][0] == 'buy '):
            #         last_buy = float(history[-1][3])
            #         last_sell= cl_array[-1]
            #     else:
            #         last_buy  = float(history[-1][4])
            #         last_sell = float(history[-1][3] )
            
        action = 0

        



def time_now(type_time = 'str'):
    
        if(type_time == 'str'):
            named_tuple = time.localtime()
            time_str = time.strftime("%m/%d_%H:%M", named_tuple) 
            return time_str
    
    

def log( currency_name , typ = 'read', old_history = []):
    
    currency_log_path = './log/'+currency_name+'-history.csv'
    
    if(typ == 'update'):
        with open(currency_log_path, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerows(old_history)
    else:
        if not(os.path.isfile(currency_log_path)):
            with open(currency_log_path ,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['type', 'time_hms', 'Prof', 'Price', 'buy_in', 'Amount', 'RSI' , 'Total'])
                f.close()
                
        with open(currency_log_path,'a', newline='') as f:
            
            writer = csv.writer(f)
            writer.writerows([['____', '________', '____', 'START', '______', '______', '___', '____']])

        with open(currency_log_path,'r', newline='') as f:
        
            reader = csv.reader(f)
            new_history = list(reader)    
            f.close()
            return new_history
    

epoch = 0
not_action_step =0
last_buy = 'first'
last_sell = 0
b = ''
turn = 'sell' if api.usdt_percentage(currency)<50 else 'buy'
currency_market = currency + '-USDT'
history = log(currency_market)

    

print('\n##START====> '+ time_now())

while(True):
    # send_message([history[0],history[-1]])
    start = time.time()
    epoch += 1
    print('\n#########==> Epoch : ',epoch ,' ##################################\n')
    
    # cl_array  = api.live_price(currency_market)
    
    cl_array =  api.live_price2(currency, limit=250)
    
    a = np.array(ta.RSI(cl_array, RSI_PERIOD)) 
    time_str = time_now()  
    update_locals()

    if(b==''):
        if  (a[-1] >= high):
            b= 'up'
            print('up')
            not_action_step =0

        elif(a[-1] <= down):
            b= 'down'
            print('down')
            not_action_step =0
    
        elif last_buy + last_buy*0.0050 <= cl_array[-1]:
            b= 'up'
            print('+5p')
            not_action_step =0
        elif last_sell - last_sell*0.0050 >= cl_array[-1]:
            b= 'down'
            print('-5p')
            not_action_step =0
        
            
        else:
            not_action_step+=1
            
            
    if ((last_buy - last_buy*sl_ratio/100 > cl_array[-1]) and (history[-1][0] == 'buy ')):
        not_action_step =0
        print('LIMIT!!!! , sell and stop')
        sell_and_stop()
        
        # action = 1
            
    if(not_action_step >= 15): 
        high -=1.5
        down +=1.5
        not_action_step -= 10
        
        
        
    if b =='up' and (a[-1] <= a[-2]):
        action = 1
        b= ''
    
    if b =='down' and (a[-1] >= a[-2]):
        action = -1
        b= ''
        
        
        
                    
    if(action == 1 and cl_array[-1] > last_buy):
        
        if (turn == 'sell'):
                Action_func('sell')
                
            
    elif(action == -1):  
        
        if (turn == 'buy'): 
                Action_func('buy ')
                
    
    
    
    
    log(currency_market, 'update' , history )
    
    print('Time  : ',time_str)
    print('RSI   : ',a[-1])
    print('USDT  : ', "{:.4f}".format(float(api.currency_Inventory('usdt')))) 
    try:
        print('Currency: ', "{:.5f}".format(float(api.currency_Inventory(currency))))   
    except :pass
    print('Price : ' , cl_array[-1])        
    print(*history, sep = "\n")
    end = time.time()

    if ((end - start)<60):
        time.sleep(60 - (end - start))
                
            
            
            
            
     
            
            
            
            
            
            
            
            
            
