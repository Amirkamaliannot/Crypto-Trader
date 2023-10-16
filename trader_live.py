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
import share
# from get_log import send_message


# defining local variable #

currency = share.currency
RSI_PERIOD = 14
# trans_ratio = 6/10
high =63
down =37
sl_ratio = 0.8



#this function can sell currencies immediately when encounter Stop_Lost_Limit

def sell_and_stop(mod):
    
    global last_buy , last_sell, history , time_str, cl_array, not_sell_step, local_max, b
    b = ''
    
    temp_amount = "{:.3f}".format(float(api.currency_Inventory(currency))*99/100)
    is_sell = api.sell(currency_market ,temp_amount )
    if (is_sell):
        history.append(['sell',time_str, str("{:.2f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1],last_buy, float(temp_amount)*cl_array[-1] ,str(int(a[-1]))+' _ '+str(mod), api.total_money()]) 
        print('limit')
        last_sell = cl_array[-1]
        not_sell_step = 0
        local_max = cl_array[-1]

    else: 
        print('god FMe !!!! doesn,t sell , do something')
        exit()
        
    temp_price = cl_array[-1]
    time.sleep(120)
    cl_array = api.live_price2(currency, limit=1)
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
    
        
# this is for sell and buy simply  :))
 
def Action_func(type_action):
        
        global last_sell,last_buy, local_min, local_max, total_cash, total_bit, high, down, turn, not_sell_step
        
        
        
        if  (type_action == 'sell'):

            
            temp_amount = 'all'#"{:.2f}".format(float(api.currency_Inventory(currency))*99/100)
            
            is_sell = api.sell(currency_market ,temp_amount )
            if (is_sell):
                history.append(['sell',time_str, str("{:.3f}".format((cl_array[-1]-last_buy)/last_buy*100))+'%', cl_array[-1],last_buy, float("{:.2f}".format(float(temp_amount)))*cl_array[-1] ,int(a[-1]) ,api.total_money()]) 
                print('sell')
                turn = 'buy'
                # send_message([history[0],history[-1]])
                
            else: print('ops not sell , wrong ', temp_amount )

            last_sell = cl_array[-1]
            not_sell_step = 0
            local_max = cl_array[-1]
            high =61

            
        elif(type_action == 'buy '):
            
            temp_amount = 'all'#"{:.2f}".format(float(api.currency_Inventory('usdt'))*99/100)
            
            is_buy = api.buy(currency_market ,temp_amount )
            if (is_buy):
                history.append(['buy ',time_str, '-----', cl_array[-1],'------', "{:.2f}".format(float(temp_amount)), int(a[-1]) ,api.total_money()]) 
                print('buy')
                turn = 'sell'
                # send_message([history[0],history[-1]])
            else: print('ops not buy , wrong',  temp_amount )

            last_buy = cl_array[-1]
            down =39
            high =61
            local_max = cl_array[-1]

# some local variable should updating in each iteration 

def update_locals():
        global last_buy ,last_sell, action, local_max,local_min
        
        
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
        if (local_max < cl_array[-1]):
            local_max = cl_array[-1]
            
        # if (local_min > cl_array[-1]):
        #     local_min = cl_array[-1]
            
        action = 0

        


# Current time in form of string 
def time_now(type_time = 'str'):
    
        if(type_time == 'str'):
            named_tuple = time.localtime()
            time_str = time.strftime("%m/%d_%H:%M", named_tuple) 
            return time_str
    
    
# recording history or load them for first epoch
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
                writer.writerow(['type ', ' time_ hms ', 'Prof', 'Price', 'buy_in', 'Amount', 'RSI' , 'Total'])
                f.close()
                
        with open(currency_log_path,'a', newline='') as f:
            
            writer = csv.writer(f)
            writer.writerows([['START', time_now(), '____', 'START', '______', '______', '___', '_____']])

        with open(currency_log_path,'r', newline='') as f:
        
            reader = csv.reader(f)
            new_history = list(reader)    
            f.close()
            return new_history
    
# other nonsignificant variables
epoch = 0
not_action_step =0
not_sell_step = 0
last_buy = 'first'
last_sell = 0
b = ''
local_min = 0
local_max = 0
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
    
    cl_array =  api.live_price2(currency, limit=40).astype(float)
    
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
        
            
        else:
            not_action_step+=1
            
            
    if(turn == 'sell'):
        not_sell_step+=1
    #for Smart Stop loss
    ########################### THIS MOST ADD
    
    if (history[-1][0] == 'buy '):
        profit = ( local_max - last_buy )/last_buy
        
        # limit_loss = 0
        # mod = 0
        if profit < (0.2 / 100):#  and ((mv[-1]-mv[-2])<(mv[-5]-mv[-6])) and (mv[-1] > mv[-2])):
            
            # limit_loss = last_buy * (100-sl_ratio) / 100
            limit_loss = 0
            mod = 1
            
        elif(profit >= (0.2/100) and profit< (0.7/100)):
            
            # limit_loss = last_buy
            limit_loss = 0
            mod = 2
        
        elif(profit >= (0.6/100)):
            limit_loss = local_max - last_buy* 0.4/100
            limit_loss = 0
            mod = 3
            print(profit)
        
                
                
        if ((limit_loss > cl_array[-1])): #or (not_sell_step >180 and (cl_array[-1] < last_buy*(1 - sl_ratio/100) and mv[-1] < mv[-4]))):
            not_action_step =0
            print('LIMIT!!!! , sell and stop')
            sell_and_stop(mod)
        
        # action = 1
    
    if(not_action_step >= 15): 
        high -=0.25
        down +=0.25
        not_action_step -= 10
        
        
        
    if b =='up' and (cl_array[-1] < cl_array[-2]):
        action = 1
        b= '' 
    
    if b =='down' and (cl_array[-1] > cl_array[-2]):
        action = -1
        b= ''
        
        
        
                    
    if(action == 1):# and cl_array[-1] > last_buy):
        
        if (turn == 'sell'):
                Action_func('sell')
                
            
    elif(action == -1):  
        
        if (turn == 'buy'): 
                Action_func('buy ')
                
    
    
    log(currency_market, 'update' , history )
    
    print('Time  : ',time_str)
    print('RSI   : ',a[-1])
    print('USDT  : ', "{:.4f}".format(api.assets)) 
    try:
        print('Currency: ', "{:.5f}".format(api.currency))   
    except :pass
    print('Price : ' , cl_array[-1])      
    print('Price : ' , api.total_money())      
    print(*history, sep = "\n")
    end = time.time()

    if ((end - start)<60):
        time.sleep(60 - (end - start))



