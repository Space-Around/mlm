import telebot
from Crypto.Cipher import AES
import json
import config
import paypal
import sqlite3
import datetime
import aes
import random
import db
import string

bot = telebot.TeleBot(config.TOKEN)
bot.remove_webhook()

def activate(key, user_id, user_name, chat_id):        
    if len(key) == 16:
        user_info = db.get_user_info(key)        

        if user_info != False:                         
            if user_info['lvl_1_payed'] == 1:                
                bot.send_message(chat_id, "Ваш ключ уже активирован")
                return                 
            
            user_info['tg_user_id'] = user_id
            user_info['tg_user_name'] = user_name
            user_info['tg_chat_id'] = chat_id
            
            db.update_user_info(user_info)

            action = "activate"

            encrypted_key = aes.encrypt(user_info['key'] + " " + action)

            json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_1_AMOUNT, debug=False)

            bot.send_message(chat_id, "Перейдите по ссылке для оплаты:\n" + response.result.links[1].href)
        else:
            bot.send_message(chat_id, "Такого ключа не существует")            
    else:
        bot.send_message(chat_id, "Неверный формат ключа")
    
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def gen(data, user_id, user_name, chat_id):    
    paypal_account = data.split()[0]
    email_account = data.split()[1]

    if db.get_user_info_by_tg_id(user_id):
        key = ""

        while True:
            key = randomword(16)
            if db.check_key(key) == False:
                break

        user_info = db.get_user_info_by_tg_id(user_id)
        user_info['key_gen'] = user_info['key_gen'] + 1
        # print(user_info)
        db.update_user_info(user_info)

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

        db.insert_user_info(new_user_info)

        bot.send_message(chat_id, "Оправьте ключ новому пользователю для активации.\n\nКлюч: " + key)


    # paypal_account = data.split()[0]
    # email_account = data.split()[1]
    # else:
        # bot.send_message(chat_id, "Вы не можете генерировать ключи, так как Вас нету в системе, попросите Ваших друзей или знакомых сгенерировать ключ для Вас")



    # if aes.decrypt(data_key) != False:
    #     json_data = aes.decrypt(data_key)
    #     lvl_index = json_data["pay"]["lvlInfo"]["key"]["current"] - 1
        

    #     if json_data["pay"]["lvlInfo"]["key"]["infinit"] == 1:
    #         with open("./key_struct.json") as f:
    #                 data_key_new = json.load(f)

    #         data_key_new["id"] = str(random.randint(1000, 9999)) + str(random.randint(1000, 9999)) + str(random.randint(1000, 9999)) + str(random.randint(1000, 9999))
    #         data_key_new["user"]["paypal"] = paypal_account
    #         data_key_new["user"]["email"] = email_account
            
    #         data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["telegram"]["userName"] = user_name
    #         data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["telegram"]["id"] = user_id
    #         data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["telegram"]["chatId"] = chat_id
    #         data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["email"] = json_data["user"]["email"]
    #         data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["paypal"] = json_data["user"]["paypal"]

    #         encrypt_data = aes.encrypt(json.dumps(data_key_new))

    #         bot.send_message(chat_id, "Оправьте ключ новому пользователю для активации.\n\nКлюч: " + encrypt_data)

    #         return
                
    #     if json_data["pay"]["lvlInfo"]["lvl"][lvl_index]["payed"] == 1:
    #         if json_data["pay"]["lvlInfo"]["key"]["current"] <= json_data["pay"]["lvlInfo"]["key"]["max"]:
    #             json_data["pay"]["lvlInfo"]["key"]["current"] = json_data["pay"]["lvlInfo"]["key"]["current"] + 1
    #             with open("./key_struct.json") as f:
    #                 data_key_new = json.load(f)

    #             data_key_new["id"] = str(random.randint(1000, 9999)) + str(random.randint(1000, 9999)) + str(random.randint(1000, 9999)) + str(random.randint(1000, 9999))
    #             data_key_new["user"]["paypal"] = paypal_account
    #             data_key_new["user"]["email"] = email_account
                
    #             data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["telegram"]["userName"] = user_name
    #             data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["telegram"]["id"] = user_id
    #             data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["email"] = json_data["user"]["email"]
    #             data_key_new["pay"]["lvlInfo"]["lvl"][0]["seller"]["paypal"] = json_data["user"]["paypal"]

    #             encrypt_data = aes.encrypt(json.dumps(data_key_new))

    #             bot.send_message(chat_id, "Оправьте ключ новому пользователю для активации.\n\nКлюч: " + encrypt_data)
    #             bot.send_message(chat_id, "Оправьте ключ новому пользователю для активации.\n\nКлюч: " + encrypt_data)
    #         else:
    #             bot.send_message(chat_id, "Вы достигли максимально количества генерация ключей на данном уровне, чтобы генерировать больше клюей необходимо повысить уровень ключа")
    #     else:
    #         bot.send_message(chat_id, "Ваш ключ не активен, необходимо произвести оплату для его активации")
    # else:
    #     bot.send_message(chat_id, "Неверный формат ключа")

def upgrade(user_id, user_name, chat_id):
    user_info = db.get_user_info_by_tg_id(user_id)

    if user_info['lvl'] == 1:
        action = "upgrade_to_lvl_2"
        encrypted_key = aes.encrypt(user_info['key'] + " " + action)
        json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_2_AMOUNT, debug=False)
    
    if user_info['lvl'] == 2:
        action = "upgrade_to_lvl_3"
        json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_3_AMOUNT, debug=False)

    if user_info['lvl'] == 3:
        action = "upgrade_to_lvl_4"
        json_data_order, response = paypal.CreateOrder().create_order(encrypted_key, config.LVL_4_AMOUNT, debug=False)


    bot.send_message(chat_id, "Перейдите по ссылке для оплаты:\n" + response.result.links[1].href)
    

@bot.message_handler(commands=['start'])
def handler_start(message):
    print(message)

@bot.message_handler(commands=['help'])
def handler_help(message):
    pass

@bot.message_handler(commands=['activate'])
def handler_activate(message):   
    chat_id = message.chat.id

    bot.send_message(chat_id, "Втавьте ключ для его активации, ответив на это сообщение")


@bot.message_handler(commands=['upgrade'])
def handler_upgrade(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username

    user_info = db.get_user_info_by_tg_id(user_id)

    if user_info == False:
        bot.send_message(chat_id, "Вы не можете генерировать ключи, так как Вас нету в системе, попросите Ваших друзей или знакомых сгенерировать ключ для Вас")
        return

    if user_info['lvl'] == 4:
        bot.send_message(chat_id, "Вы достигли максимального уровня")
        return    

    upgrade(user_id, user_name, chat_id)
    


@bot.message_handler(commands=['gen'])
def handler_gen(message):
    user_info = db.get_user_info_by_tg_id(message.from_user.id)

    if user_info != False:
        if (user_info['lvl_1_payed'] == 1):
            if user_info['lvl'] == 4 or (user_info['lvl'] == 1 and user_info['key_gen'] <= 4)  or (user_info['lvl'] == 2 and user_info['key_gen'] <= 8) or (user_info['lvl'] == 3 and user_info['key_gen'] <= 33):
                bot.send_message(message.chat.id, "Введите PayPal и Email нового пользователя, ответив на это сообщение, в строго заданном формате, соблюдая пробелы.\n\nФормат:\npaypal@example.com mail@example.com") 
            else:
                bot.send_message(message.chat.id, "Вы достигли максимального количества генераций на данном уровне, воспользуйтьесь командой /upgrade для повышения уровня") 
        else: 
            bot.send_message(message.chat.id, "Вы не можете генерировать ключи, актвируйте свой ключ при помощи команды /activate") 
    else:
        bot.send_message(chat_id, "Вы не можете генерировать ключи, так как Вас нету в системе, попросите Ваших друзей или знакомых сгенерировать ключ для Вас")



@bot.message_handler(commands=['info'])
def handler_info(message):
    pass

@bot.message_handler(commands=['pay'])
def handler_pay(message):
    pass


@bot.message_handler(content_types=['text'])
def handle_text(message):
    activate_reply = "Втавьте ключ для его активации, ответив на это сообщение"
    gen_reply = "Введите PayPal и Email нового пользователя, ответив на это сообщение, в строго заданном формате, соблюдая пробелы.\n\nФормат:\npaypal@example.com mail@example.com"

    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username

    if message.reply_to_message.text == activate_reply:      
        key = message.text.strip()
        activate(key, user_id, user_name, chat_id)    

    if message.reply_to_message.text == gen_reply:
        gen(message.text, user_id, user_name, chat_id)   
    

bot.polling()


