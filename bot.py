#!/usr/bin/python
# -*- coding: utf-8 -*-
import db
import aes
import json
import paypal
import config
import string
import random
import sqlite3
import telebot
import logging
import datetime

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

logging.basicConfig(filename="bot.log", level=logging.ERROR, format=_log_format)

try:
    bot = telebot.TeleBot(config.TOKEN)
    logging.info("start telegram bot")

    bot.remove_webhook()
    logging.info("remove webhook")

    dbconn = db.DBConnection()
    logging.info("connect to db")

except BaseException as msg:
    logging.error(msg)

def activate(key, user_id, user_name, chat_id):      
    try:  
        if len(key) == 16:
            user_info = dbconn.get_user_info(key)        
            logging.info("[activate] get user info by key from db | key: " + str(key))

            if user_info != False:      
                seller = dbconn.get_user_info_by_tg_id(user_id)
                logging.info("[activate] get user info by telegram id | user_id: " + str(user_id))

                if seller != False:
                    if user_info['seller_1_id'] == seller['id']:
                        bot.send_message(chat_id, "Вы не можете активировать ключ, который сами сгенерировали")
                        logging.info("[activate] send message that faild activation because own gen | chat_id: " + str(chat_id))
                        return  

                    if (dbconn.get_user_info_by_tg_id(user_id)['key'] != key) and (len(dbconn.get_user_info_by_key(key)['tg_user_id']) > 0):
                        bot.send_message(chat_id, "Вы патаетесь активировать ключ другого пользователя")
                        logging.info("[activate] send message that failed activation because activation froud key | chat_id: " + str(chat_id))
                        return

                    if user_info['lvl_1_payed'] == 1:                
                        bot.send_message(chat_id, "Ваш ключ уже активирован")
                        logging.info("[activate] send message that failed activation beacuse own key has active yet | chat_id: " + str(chat_id))
                        return                 
                
                user_info['tg_user_id'] = user_id
                user_info['tg_user_name'] = user_name
                user_info['tg_chat_id'] = chat_id
                
                dbconn.update_user_info(user_info)
                logging.info("[activate] update user info in db | user_info" + str(user_info))

                action = "activate"

                encrypted_key = aes.AESData().encrypt(user_info['key'] + " " + action)

                json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_1_AMOUNT, debug=False)
                logging.info("[activate] create order | link: " + str(response.result.links[1].href))


                bot.send_message(chat_id, "Перейдите по ссылке для оплаты:\n" + response.result.links[1].href)
                logging.info("[activate] send message with paypal link | chat_id: " + str(chat_id))
            else:
                bot.send_message(chat_id, "Такого ключа не существует")           
                logging.info("[activate] send message that key doesnt exist | chat_id: " + str(chat_id))

        else:
            bot.send_message(chat_id, "Неверный формат ключа")
            logging.info("[activate] send message that invalid key format | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)
    
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def gen(data, user_id, user_name, chat_id):    
    try:
        paypal_account = data.split()[0]
        email_account = data.split()[1]

        if dbconn.get_user_info_by_tg_id(user_id):
            logging.info("[gen] get user info by telegram id | user_id" + str(user_id))

            key = ""

            while True:
                key = randomword(16)
                if dbconn.check_key(key) == False:
                    break

            logging.info("[gen] gen key and check in db | key: " + str(key))

            user_info = dbconn.get_user_info_by_tg_id(user_id)
            logging.info("[gen] get user info by telegram id | user_id: " + str(user_id))
            
            user_info['key_gen'] = int(user_info['key_gen']) + 1

            dbconn.update_user_info(user_info)
            logging.info("[gen] update user info in db | user_info: " + str(user_info))

            new_user_info = {
                'key': key,
                'tg_chat_id': "",
                'tg_user_name': "",
                'tg_user_id': "",
                'paypal': paypal_account,
                'email': email_account,
                'lvl': 0,
                'key_gen': 0,
                'seller_1_id': user_info['id'],
                'seller_2_id': user_info['seller_1_id'],
                'seller_3_id': user_info['seller_2_id'],
                'seller_4_id': user_info['seller_3_id'],
                'lvl_1_payed': 0,
                'lvl_2_payed': 0,
                'lvl_3_payed': 0,
                'lvl_4_payed': 0
            }

            dbconn.insert_user_info(new_user_info)
            logging.info("[gen] insert new user info in db | new user info: " + str(new_user_info))

            bot.send_message(chat_id, "Оправьте ключ новому пользователю для активации.\n\nКлюч: " + key)
            logging.info("[gen] send message with new gen key | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)

def upgrade(user_id, user_name, chat_id):
    try:
        user_info = dbconn.get_user_info_by_tg_id(user_id)    
        logging.info("[upgrade] get user info by telegram id | user_id" + str(user_id))

        if int(user_info['lvl']) == 1 and int(user_info['key_gen']) == 4:
            action = "upgrade_to_lvl_2"
            encrypted_key = aes.AESData().encrypt(user_info['key'] + " " + action)
            json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_2_AMOUNT, debug=False)
            logging.info("[upgrade] create order for 2 lvl | link: " + str(response.result.links[1].href))
            bot.send_message(chat_id, "Перейдите по ссылке для оплаты:\n" + response.result.links[1].href)
            logging.info("[upgrade] send message wirh paypal link | chat_id: " + str(chat_id))
        
        elif int(user_info['lvl']) == 2 and int(user_info['key_gen']) == 8:
            action = "upgrade_to_lvl_3"
            encrypted_key = aes.AESData().encrypt(user_info['key'] + " " + action)
            json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_3_AMOUNT, debug=False)
            logging.info("[upgrade] create order for 3 lvl | link: " + str(response.result.links[1].href))
            bot.send_message(chat_id, "Перейдите по ссылке для оплаты:\n" + response.result.links[1].href)  
            logging.info("[upgrade] send message with paypal link | chat_id" + str(chat_id))

        elif int(user_info['lvl']) == 3 and int(user_info['key_gen']) == 33:
            action = "upgrade_to_lvl_4"
            encrypted_key = aes.AESData().encrypt(user_info['key'] + " " + action)
            json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_4_AMOUNT, debug=False)
            logging.info("[upgrade] create order 4 lvl | link: " + str(response.result.links[1].href))
            bot.send_message(chat_id, "Перейдите по ссылке для оплаты:\n" + response.result.links[1].href)
            logging.info("[upgrade] send message with paypal link | chat_id: " + str(chat_id))
        else:
            bot.send_message(chat_id, "Вы не можете повысить уровень, необходимо достигнуть максимального количества генерация на данном уровне")
            logging.info("[upgrade] send message that user can't update lvl beacuse his lvl is max | chat_id: " + str(chat_id))
            return

    except BaseException as msg:
        logging.error(msg)
    

@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        chat_id = message.chat.id
        user_name = message.from_user.username
        if user_name is None:
            bot.send_message(chat_id, "Здравствуй! Если у тебя уже есть ключ, то воспользуйся командой /activate")
        else:
            bot.send_message(chat_id, "Здравствуй, " + str(user_name) + "! Если у тебя уже есть ключ, то воспользуйся командой /activate")

        logging.info("[cmd start] command start | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)

@bot.message_handler(commands=['help'])
def handler_help(message):
    try:
        chat_id = message.chat.id
        user_name = message.from_user.username
        message_text = "Если у Вас возникли какие-то проблемы, тогда Вы можете связаться с администрацией.\nTelegram: " + config.ADMINE_TELEGRAM + "\nEmail: " + config.ADMINE_EMAIL + "\n\nОписание команд:\nstart - Приветсвенное сообщение, сообщающее о согласии пользователя с условиями использования бота\nhelp - Получить контакты для связи с администрацией, также узнать подробное описание всех комманд\nactivate - Активация ключа, используется один раз перед началом работы с ботом для последующей генерации ключей\nupgrade - Увеличить свой уровень на один, используется, только в том случае, когда пользователь достиг максимального количества генераций ключей на текущем уровне\ngen - Генерация ключа, используется исключительно для создания ключей первого уровня\ninfo - Получить детальную информацию о ключе\n\nFAQ's:\n1)Как отвечать на сообщения?\nWindows и Linux:\nНажативем правой кнопки мыши на сообщение, после чего появиться всплывающее меню с пунктом Ответить\nAndroid и IOS:\nКороткое нажатие на сообщение, после чего появится всплывающее меню с пунктом Ответить/Reply\n2)Как изменить свой PayPal:\nОбратитесь к администратору\n3)Как изменить свой Email:\nОбратитесь к администратору\n4)Как вернуть денежные средства после активации или покупки нового уровня:\nДанной возможности нету, ознакомьтесь с условиями соглашения"
        bot.send_message(chat_id, message_text)

        logging.info("[cmd help] command help | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)
    

@bot.message_handler(commands=['activate'])
def handler_activate(message):   
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id

        user_info = dbconn.get_user_info_by_tg_id(user_id)
        logging.info("[cmd activate] get user info by telegram id | user_id: " + str(user_id))

        if user_info == False:
            bot.send_message(chat_id, "Втавьте ключ для его активации, ответив на это сообщение, активировав ключ Вы соглашаетесь со всеми условиями использования бота")
            logging.info("[cmd activate] send message for key activation | chat_id: " + str(chat_id))
        else:
            bot.send_message(chat_id, "Ваш ключ уже активирован")
            logging.info("[cmd activate] command activate, own key has activate yes | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)


@bot.message_handler(commands=['upgrade'])
def handler_upgrade(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = message.from_user.username

        user_info = dbconn.get_user_info_by_tg_id(user_id)
        logging.info("[cmd upgrade] get user info by telegram id | user_id: " + str(user_id))

        if user_info == False:
            bot.send_message(chat_id, "Вы не можете использовать эту команду, так как Вас нету в системе")
            logging.info("[cmd upgrade] send message that user is not in the system | chat_id: " + str(chat_id))
            return

        if int(user_info['lvl']) == 4:
            bot.send_message(chat_id, "Вы достигли максимального уровня")
            logging.info("[cmd upgrade] send message that user has max lvl | chat_id: " + str(chat_id))
            return    

        upgrade(user_id, user_name, chat_id)    

    except BaseException as msg:
        logging.error(msg)


@bot.message_handler(commands=['gen'])
def handler_gen(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_info = dbconn.get_user_info_by_tg_id(user_id)
        logging.info("[cmd gen] get user info by telegram id | user_id: " + str(user_id))

        if user_info != False:        
            if (int(user_info['lvl_1_payed']) == 1):
                if int(user_info['lvl']) > 1 or (int(user_info['lvl']) == 1 and int(user_info['key_gen']) < 4):
                    bot.send_message(message.chat.id, "Введите PayPal и Email нового пользователя, ответив на это сообщение, в строго заданном формате, соблюдая пробелы.\n\nФормат:\npaypal@example.com mail@example.com") 
                    logging.info("[cmd gen] send a message asking for paypal and email | chat_id: " + str(chat_id))
                else:
                    bot.send_message(message.chat.id, "Вы достигли максимального количества генераций на данном уровне, воспользуйтьесь командой /upgrade для повышения уровня") 
                    logging.info("[cmd gen] send message that user get max count of gen | chat_id: " + str(chat_id))
            else: 
                bot.send_message(message.chat.id, "Вы не можете генерировать ключи, актвируйте свой ключ при помощи команды /activate") 
                logging.info("[cmd gen] send message that user can't gen key beacuse to activate it first | chat_id: " + str(chat_id))
        else:
            bot.send_message(message.chat.id, "Вы не можете генерировать ключи, так как Вас нету в системе, попросите Ваших друзей или знакомых сгенерировать ключ для Вас")
            logging.info("[cmd gen] send message that user can't gen key because it's not in the system | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)


@bot.message_handler(commands=['info'])
def handler_info(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_info = dbconn.get_user_info_by_tg_id(user_id)
        logging.info("[cmd info] get user info by telegram id from db | user_id: " + str(user_id))

        max_key_gen = 0

        if int(user_info['lvl']) == 1:
            max_key_gen = 4

        if int(user_info['lvl']) == 2:
            max_key_gen = 8

        if int(user_info['lvl']) == 3:
            max_key_gen = 33

        if int(user_info['lvl']) == 4:
            max_key_gen = "бесконечности"

        if user_info != False:
            bot.send_message(chat_id, "Информация о ключе:\nУровень: " + str(user_info['lvl']) + "\nСгенерированно на данном уровне: " + str(user_info['key_gen']) + " из " + str(max_key_gen) + "\nКлюч: " + user_info['key'] + "\nPayPal: "+ user_info['paypal'] + "\nEmail: " + user_info['email'])
            logging.info("[cmd info] send message with info about acc | chat_id: " + str(chat_id))

    except BaseException as msg:
        logging.error(msg)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    activate_reply = "Втавьте ключ для его активации, ответив на это сообщение, активировав ключ Вы соглашаетесь со всеми условиями использования бота"
    gen_reply = "Введите PayPal и Email нового пользователя, ответив на это сообщение, в строго заданном формате, соблюдая пробелы.\n\nФормат:\npaypal@example.com mail@example.com"

    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username
    
    # try:
    if message.reply_to_message != None:
        if message.reply_to_message.text == activate_reply:      
            key = message.text.strip()
            activate(key, user_id, user_name, chat_id)    

        if message.reply_to_message.text == gen_reply:
            gen(message.text, user_id, user_name, chat_id)   
    # except:
        # bot.send_message(chat_id, "Произошла ошибка. Попробуйте ещё раз, если ошибка не исчезла, тогда обратитесь к администрации")
    

bot.polling()


