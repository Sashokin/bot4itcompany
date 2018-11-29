# -*- coding: utf-8 -*-
from telebot import types

btn_main_menu = types.KeyboardButton('🚪Главное меню')
btn_back_main_menu = types.KeyboardButton('🚪Вернуться в главное меню')

main_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_ord_phone = types.KeyboardButton('📱Заказать звонок')
btn_price = types.KeyboardButton('📜Расчет стоимости')
btn_chat = types.KeyboardButton('✉️Чат с оператором')
btn_help = types.KeyboardButton('❓О нас')
main_menu.row(btn_ord_phone, btn_price)
main_menu.row(btn_chat, btn_help)

phone_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_phone = types.KeyboardButton(text='📱Отправить номер телефона', request_contact=True)
phone_page.add(btn_phone, btn_back_main_menu)

send_mes_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
send_mes_page.add(btn_back_main_menu)
