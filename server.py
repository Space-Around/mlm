# examples/server_simple.py
from aiohttp import web
import ssl
import paypal
import telebot
import config
import sqlite3
import aes
import datetime
import json
from dateutil.parser import parse
import db

bot = telebot.TeleBot(config.TOKEN)

WEBHOOK_PORT = 88  
WEBHOOK_LISTEN = '10.168.0.6'

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

ACTIONE_ACTIVATE = "activate"
ACTIONE_UPGRADE_LVL_2 = "upgrade_to_lvl_2"
ACTIONE_UPGRADE_LVL_3 = "upgrade_to_lvl_3"
ACTIONE_UPGRADE_LVL_4 = "upgrade_to_lvl_4"

def activate(key, token):

    response = paypal.AuthorizeOrder().authorize_order(token, debug=False)

    if response.status_code == 201:
        authorization_id = response.result.purchase_units[0].payments.authorizations[0].id


        user_info = db.get_user_info(key)

        user_info['lvl_1_payed'] = 1
        user_info['key_gen'] = 0
        user_info['lvl'] = 1

        bot.send_message(user_info['tg_chat_id'], "Оплата прошла успешна. Активирован 1ый уровень.")

        seller = db.get_user_info_by_id(user_info['seller_1_id'])

        create_response = paypal.CreatePayouts().create_payouts(seller['paypal'], config.LVL_1_AMOUNT, False)

        bot.send_message(seller['tg_chat_id'], "Пользователь " + user_info['tg_user_name'] + " приобрёл ключ 1ого уровня за " + config.LVL_1_AMOUNT + "$")

def upgrade(lvl, key, token): 
    response = paypal.AuthorizeOrder().authorize_order(token, debug=False)

    if response.status_code == 201:
        authorization_id = response.result.purchase_units[0].payments.authorizations[0].id
        message_text = ""
        user_info = db.get_user_info(key)

        if lvl = 2:
            user_info['lvl_2_payed'] = 1
            message_text = "Оплата прошла успешна. Активирован 2ой уровень."

            seller = db.get_user_info_by_id(user_info['seller_2_id'])

            create_response = paypal.CreatePayouts().create_payouts(seller['paypal'], config.LVL_2_AMOUNT, False)

            bot.send_message(seller['tg_chat_id'], "Пользователь " + user_info['tg_user_name'] + " приобрёл ключ 2ого уровня за " + config.LVL_2_AMOUNT + "$")
        
        if lvl = 3:
            user_info['lvl_3_payed'] = 1
            message_text = "Оплата прошла успешна. Активирован 3ий уровень."

            seller = db.get_user_info_by_id(user_info['seller_3_id'])

            create_response = paypal.CreatePayouts().create_payouts(seller['paypal'], config.LVL_3_AMOUNT, False)

            bot.send_message(seller['tg_chat_id'], "Пользователь " + user_info['tg_user_name'] + " приобрёл ключ 3его уровня за " + config.LVL_3_AMOUNT + "$")

        if lvl = 4:
            user_info['lvl_4_payed'] = 1
            message_text = "Оплата прошла успешна. Активирован 4ый уровень."

            seller = db.get_user_info_by_id(user_info['seller_4_id'])

            create_response = paypal.CreatePayouts().create_payouts(seller['paypal'], config.LVL_4_AMOUNT, False)

            bot.send_message(seller['tg_chat_id'], "Пользователь " + user_info['tg_user_name'] + " приобрёл ключ 4ого уровня за " + config.LVL_4_AMOUNT + "$")

            
        user_info['lvl'] = lvl
        user_info['key_gen'] = 0

        bot.send_message(user_info['tg_chat_id'], message_text)
        

async def handle(request):

    token = request.rel_url.query.get('token', '')
    encrypted_key = request.rel_url.query.get('encrypted_key', '')
    decrypted_data = aes.decrypt(encrypted_key)

    key = decrypted_data.split()[0]
    action = decrypted_data.split()[1]

    if action == ACTIONE_ACTIVATE:
        activate(key, token)

    if action == ACTIONE_UPGRADE_LVL_2:
        upgrade(2, key, token)

    if action == ACTIONE_UPGRADE_LVL_3:
        upgrade(3, key, token)

    if action == ACTIONE_UPGRADE_LVL_4:
        upgrade(4, key, token)

    text = "Дождитесь редиректа в telegram"
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    web.run_app(
        app,
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=context,
    )