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

async def handle(request):
    # user_action = request.rel_url.query.get('paypal_auth', '')
    # print(request.rel_url.query.get('PayerID', ''))

    token = request.rel_url.query.get('token', '')
    encrypted_key = request.rel_url.query.get('encrypted_key', '')
    decrypted_data = aes.decrypt(encrypted_key)

    key = decrypted_data.split()[0]
    action = decrypted_data.split()[1]

    if action == ACTIONE_ACTIVATE:
        activate(key, token)

    if action == ACTIONE_UPGRADE_LVL_2:
        upgrade
        pass

    if action == ACTIONE_UPGRADE_LVL_3:
        pass

    if action == ACTIONE_UPGRADE_LVL_4:
        pass

    # if len(token) > 0:
    #     # response = paypal.AuthorizeOrder().authorize_order(token, debug=False)        

    #     # if response.status_code == 201:
    #         # conn = sqlite3.connect('paypal.db')
    #         # c = conn.cursor()
    #         # res = c.execute("SELECT * FROM orders WHERE ")
    #         # data = res.fetchall()

    #         # authorization_id = response.result.purchase_units[0].payments.authorizations[0].id
    #         # if aes.decrypt(data) != False:
    #         json_data = aes.decrypt(data_key)

    #         print(json_data)

    #         if json_data["pay"]["lvlInfo"]["lvl"][0]["payed"] == 0:

    #             json_data["pay"]["lvlInfo"]["key"]["max"] = 4
    #             json_data["pay"]["lvlInfo"]["key"]["current"] = 0

    #             json_data["pay"]["lvlInfo"]["lvl"][0]["date"] = datetime.datetime.now().strftime('%Y-%m-%d')

    #             json_data["pay"]["lvlInfo"]["lvl"][0]["payed"] = 1                

    #             # create_response = paypal.CreatePayouts().create_payouts(json_data["pay"]["lvlInfo"]["lvl"][0]["seller"]["paypal"], json_data["pay"]["lvlInfo"]["lvl"][0]["amount"], False)

    #             data_key_new = aes.encrypt(json_data)

    #             bot.send_message(json_data["pay"]["lvlInfo"]["lvl"][0]["seller"]["telegram"]["chatId"], "Пользователь " + json_data["user"]["telegram"]["userName"] + " приобрёл ключ 1ого уровня за " + json_data["pay"]["lvlInfo"]["lvl"][0]["amount"] + "$")
    #             bot.send_message(chat_id, "Оплата прошла успешна. Активирован 1ый уровень.\n\n Ключ: " + data_key_new)

    #         elif json_data["pay"]["lvlInfo"]["lvl"][1]["payed"] == 0:
    #             pass

    #         elif json_data["pay"]["lvlInfo"]["lvl"][2]["payed"] == 0:
    #             pass

    #         elif json_data["pay"]["lvlInfo"]["lvl"][3]["payed"] == 0:
    #             pass

    #         # bot.send_message(chat_id, "Оплата прошла успешна. Активирован 1ый уровень")
    #             # cur.execute("UPDATE orders SET id_auth = ?, date_auth = ? WHERE id = ?", (authorization_id, datetime.datetime.now(), res.fetchall()[i][0]))        
    #             # con.commit()

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