# -*- coding: utf-8 -*-
from peewee import *


db = SqliteDatabase('database_it.db')


class User(Model):
    id = CharField()  # id пользователя
    phone = CharField()  # телефон пользователя
    send_phone = CharField()  # необходимая временная переменная(0 - дефолт, 1 - отправляет номер телефона, 2 - отправляет сообщение)

    class Meta:
        database = db


class Order(Model):
    id = CharField()  # id заказанного звонка
    user = CharField()  # заказчик
    phone = CharField()  # телефон заказчика
    type = CharField()  # тип заказа...... 0 - звонок, еще не совершен. 1 - звонок, совершен.

    class Meta:
        database = db


db.connect()
