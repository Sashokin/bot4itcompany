# -*- coding: utf-8 -*-
import telebot
from telebot import types
import my_markups
import dbhelp
import config_for_token
import time
import logging
# todo:

bot = telebot.TeleBot(config_for_token.token)  # токен спрятан в отдельном файле

# bot - @


@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as err:
        logging.error(err)
        time.sleep(5)
        print('Internet error')
