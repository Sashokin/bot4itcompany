# -*- coding: utf-8 -*-
import telebot
from telebot import types
import my_markups
import dbhelp
import config_for_token
import time
import logging
# todo: шаблоны общения, бд(уточнить), узнать название, пересоздать бота, тип пользователя

bot = telebot.TeleBot(config_for_token.token)  # токен спрятан в отдельном файле

# bot - @Tst_itcomp_bot


@bot.message_handler(commands=['start'])
def send_welcome(message):
    ccid = message.chat.id
    cb = 0
    for u in dbhelp.User.select():  # Проверяем, есть ли пользователь в базе данных
        if str(u.id) == str(ccid):
            cb = 1
    if cb == 0:  # Добавляем его
        new_user = dbhelp.User(id=ccid, phone='none', send_phone='0')
        new_user.save(force_insert=True)
    bot.send_message(ccid, '🤖Здравствуйте, я бот ...', reply_markup=my_markups.main_menu)  # дописать название фирмы


@bot.message_handler(content_types=['contact'])  # Отправление контакта при заказе обратного звонка
def contact(message):
    ccid = message.chat.id
    enter_phone = 0
    for u in dbhelp.User.select():
        if str(u.id) == str(ccid):
            if u.send_phone == '1':
                enter_phone = 1
    if enter_phone == 1:
        for u in dbhelp.User.select():
            if str(u.id) == str(ccid):
                u.phone = message.contact.phone_number
                u.send_phone = '0'
                u.save()
                id_count = 0
                for u in dbhelp.Order.select():
                    id_count += 1
                new_order = dbhelp.Order(id=id_count, user='{}'.format(ccid), phone='{}'.format(message.contact.phone_number), type='0')
                new_order.save(force_insert=True)
                bot.send_message(message.chat.id, '✅Звонок заказан, Вам позвонят в течение 10-15 минут', reply_markup=my_markups.main_menu)
                bot.send_message(config_for_token.id_manager, '✅Заказан звонок: {}'.format(message.contact.phone_number))  # Отправление информации о звонке менеджеру


@bot.message_handler(content_types=['text'])  # Основной обработчик сообщений
def main(message):
    ccid = message.chat.id
    send_phone = 0
    if message.text == '🚪Главное меню' or message.text == '🚪Вернуться в главное меню':
        for u in dbhelp.User.select():  # Очищаем все временные переменные
            if str(u.id) == str(ccid):
                u.send_phone = '0'
                u.save()
        bot.send_message(ccid, '🚪Главное меню', reply_markup=my_markups.main_menu)
    elif message.text == '📱Заказать звонок':
        for u in dbhelp.User.select():
            if str(u.id) == str(ccid):
                u.send_phone = '1'
                u.save()
        bot.send_message(ccid, '📱Оставьте номер телефона(вручную или кнопкой), чтобы менеджер смог связаться с Вами', reply_markup=my_markups.phone_page)
    elif message.text == '✉️Чат с оператором':
        bot.send_message(ccid, '✉️Отправьте сообщение или свяжитесь с менеджером напрямую - {}'.format(config_for_token.link_manager), reply_markup=my_markups.send_mes_page)
        for u in dbhelp.User.select():  # Очищаем все временные переменные
            if str(u.id) == str(ccid):
                u.send_phone = '2'
                u.save()
    else:
        for u in dbhelp.User.select():
            if str(u.id) == str(ccid):
                if u.send_phone == '1':
                    send_phone = 1
                elif u.send_phone == '2':
                    send_phone = 2
        if send_phone == 1:
            for u in dbhelp.User.select():
                if str(u.id) == str(ccid):
                    u.phone = message.text
                    u.send_phone = '0'
                    u.save()
                    id_count = 0
                    for o in dbhelp.Order.select():
                        id_count += 1
                    new_order = dbhelp.Order(id=id_count, user='{}'.format(ccid), phone='{}'.format(message.text), type='0')
                    new_order.save(force_insert=True)
                    bot.send_message(message.chat.id, '✅Звонок заказан, Вам позвонят в течение 10-15 минут', reply_markup=my_markups.main_menu)
                    bot.send_message(config_for_token.id_manager, '✅Заказан звонок: {}'.format(message.text))  # Отправление информации о звонке менеджеру
        elif send_phone == 2:
            for u in dbhelp.User.select():
                if str(u.id) == str(ccid):
                    u.send_phone = '0'
                    u.save()
                    bot.send_message(message.chat.id, '✅Сообщение успешно отправлено! Вы также можете связаться с менеджером напрямую - {}'.format(config_for_token.link_manager), reply_markup=my_markups.main_menu)
                    bot.forward_message(config_for_token.id_manager, message.chat.id, message.message_id)


while True:
    bot.polling(none_stop=True)