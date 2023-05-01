import datetime

import telebot
from telebot import types
from psycopg2 import OperationalError
import requests
import time
import json

HOST = 'http://127.0.0.1:8000'
bot = telebot.TeleBot('5915538782:AAE2ZER7pduQGDiKeAJyvPniUIKuUlO9KVM')
dct = {}


def timing(message):
    start_time = time.time()
    time.sleep(0.001)
    time_limit = 10
    while time_limit:
        time_taken = time.time() - start_time
        if time_taken < time_limit:
            bot.register_message_handler(send_message_p, message)
        else:
            time_limit = 0

    bot.send_message(message.chat.id, f'Введите пароль.')
    bot.register_next_step_handler(message, user_pass)


def send_message_p(message):
    bot.send_message(message.chat.id,
                     f"Пожалуйста, подождите. Осталось - ")


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# функция для получения данных из таблицы
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    response = requests.get(HOST + f'/api/users/{user_id}')
    if response.json():
        bot.send_message(message.chat.id, f'Здравствуйте, {response.json()["first_name"]}! Введите пароль.')
        bot.register_next_step_handler(message, user_pass)
    else:
        bot.send_message(message.chat.id, 'Здравствуйте! Пожалуйста, введите имя.')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_name = message.text.strip()
    bot.send_message(message.chat.id, 'Пожалуйста, введите фамилию.')
    bot.register_next_step_handler(message, get_surname, user_name)


def get_surname(message, user_name):
    user_last_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, get_password, user_name, user_last_name)

def success_enter(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Токарный', callback_data='lathe')
    btn2 = types.InlineKeyboardButton(text='Сверлильный', callback_data='drilling')
    btn3 = types.InlineKeyboardButton(text='Фрезерный', callback_data='milling')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите тип станка', reply_markup=markup)
    bot.register_next_step_handler(message, type_of_machine)


def get_password(message, user_name, user_last_name):
    user_password = message.text.strip()
    user_id = message.from_user.id
    response = requests.post(HOST + f"/api/users?firstname={user_name}&surname={user_last_name}&telegram_id={user_id}&password={user_password}")

    if response.json():
        bot.send_message(message.chat.id, 'Вход выполнен')
        success_enter(message)


def user_pass(message, count=3):
    user_password = message.text
    user_id = message.from_user.id
    response = requests.get(HOST + f"/api/auth?uid={user_id}&password={user_password}")
    if response.json():
        bot.send_message(message.chat.id, 'Вход выполнен')
        success_enter(message)
    else:
        count -= 1
        bot.send_message(message.chat.id, 'Неверный пароль.')
        bot.send_message(message.chat.id, f'У вас осталось попыток: {count + 1}')
        if count > 0:
            bot.register_next_step_handler(message, user_pass, count)
        else:
            bot.send_message(message.chat.id, 'Доступ запрещен')
            # timing(message)


@bot.callback_query_handler(func=lambda callback: callback.data in ["lathe", "drilling", "milling"])
def type_of_machine(callback):
    bot.answer_callback_query(callback_query_id=callback.id)
    if callback.data == 'lathe':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('SPV-500C', callback_data='SPV-500C')
        btn2 = types.InlineKeyboardButton('SPF-1500P', callback_data='SPF-1500P')
        btn3 = types.InlineKeyboardButton('Proma SM-300E', callback_data='Proma SM-300E')
        btn4 = types.InlineKeyboardButton('CU400', callback_data='CU400')
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(callback.message.chat.id, 'Выберите модель станка', reply_markup=markup)
        bot.register_next_step_handler(msg, lathe_model)

    elif callback.data == 'drilling':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('2с108п', callback_data='2с108п')
        btn2 = types.InlineKeyboardButton('B1825G', callback_data='B1825G')
        btn3 = types.InlineKeyboardButton('2М112', callback_data='2М112')
        btn4 = types.InlineKeyboardButton('ГС520', callback_data='ГС520')
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(callback.from_user.id, 'Выберите модель станка', reply_markup=markup)
        bot.register_next_step_handler(msg, drilling_model)

    elif callback.data == 'milling':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('X6142', callback_data='X6142')
        btn2 = types.InlineKeyboardButton('Optimum MT200', callback_data='Optimum MT200')
        markup.add(btn1, btn2)
        bot.send_message(callback.from_user.id, 'Выберите модель станка', reply_markup=markup)
        # bot.register_next_step_handler(callback, milling_model)


def set_machine(message, settings, id_machine):
    global dct
    if settings:
        bot.send_message(message.chat.id, f'Введите {settings[0]}')
        param1 = message.text
        dct[settings[0]] = param1
        del settings[0]
        bot.register_next_step_handler(message, set_machine, settings, id_machine)
    else:
        data = {
            "uid": message.from_user.id,
            "settings": json.dumps(dct),
            "machine_id": id_machine,
            "datetime": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        data = json.dumps(data)
        requests.post(HOST + '/api/setting', data=data)
        bot.send_message(message.chat.id, f'Ваши настройки успешно сохранены.')
        success_enter(message)


def post_settings(callback):
    response = requests.get(HOST + f'/api/machine?name={callback.data}')
    settings = json.loads(response.json()["settings"])
    id_machine = response.json()["id"]
    set_machine(callback.message, settings, id_machine)


@bot.callback_query_handler(func=lambda callback: callback.data in ["SPV-500C", "SPF-1500P", "Proma SM-300E", "CU400"])
def lathe_model(callback):
    bot.answer_callback_query(callback_query_id=callback.id)
    if callback.data == 'SPV-500C':
        post_settings(callback)
    elif callback.data == 'SPF-1500P':
        post_settings(callback)
    elif callback.data == 'Proma SM-300E':
        post_settings(callback)
    elif callback.data == 'CU400':
        post_settings(callback)


@bot.callback_query_handler(func=lambda callback: callback.data in ["2с108п", "B1825G", "2М112", "ГС520"])
def drilling_model(callback):
    bot.answer_callback_query(callback_query_id=callback.id)
    if callback.data == '2с108п':
        post_settings(callback)
    elif callback.data == 'B1825G':
        post_settings(callback)
    elif callback.data == '2М112':
        post_settings(callback)
    elif callback.data == 'ГС520':
        post_settings(callback)


@bot.callback_query_handler(func=lambda callback: callback.data in ["X6142", "Optimum MT200"])
def milling_model(callback):
    if callback.data == 'X6142':
        post_settings(callback)
    elif callback.data == 'Optimum MT200':
        post_settings(callback)


bot.polling(none_stop=True)
