# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 21:10:56 2022

@author: Amir
"""
## First :
## telegram-send --configure


import telegram_send


def send_message(string, image= None):
    try:
        telegram_send.send(messages=[string], images=image )
        return True
    except :
        return False


# import telegram

# api_key = '<your api key here>'
# user_id = '-1001542024101'

# bot = telegram.Bot(token=api_key)
# bot.send_message(chat_id=user_id, text='USP-Python has started up!')
