import db
import ssl
import aes
import time
import json
import paypal
import config
import telebot
import logging
import sqlite3
import datetime
from aiohttp import web
from paypalhttp import HttpError

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

logging.basicConfig(filename="server.log", level=logging.ERROR, format=_log_format)

try:
    bot = telebot.TeleBot(config.TOKEN)
    logging.info("start telegram bot")

    dbconn = db.DBConnection()
    logging.error("connecting to db")

except BaseException as msg:
    logging.error(msg)

WEBHOOK_PORT = 88  
WEBHOOK_LISTEN = '10.129.0.22'

WEBHOOK_SSL_CERT = './ssh/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './ssh/webhook_pkey.pem'  # Path to the ssl private key

ACTIONE_ACTIVATE = "activate"
ACTIONE_UPGRADE_LVL_2 = "upgrade_to_lvl_2"
ACTIONE_UPGRADE_LVL_3 = "upgrade_to_lvl_3"
ACTIONE_UPGRADE_LVL_4 = "upgrade_to_lvl_4"        

def activate(key, token):
    try:
        response = paypal.AuthorizeOrder().authorize_order(token, debug=False)

        logging.info("[acivation] auth order | token: " + str(token))

        if response.status_code == 201:
            authorization_id = response.result.purchase_units[0].payments.authorizations[0].id
            response_capture = paypal.CaptureOrder().capture_order(authorization_id)
            logging.info("[acivation] capture order | authorization_id: " + str(authorization_id))

            access = False
            user_info = dbconn.get_user_info(key)
            logging.info("[acivation] get user info from db by key | key: " + str(key))

            user_info['lvl_1_payed'] = 1
            user_info['key_gen'] = 0
            user_info['lvl'] = 1

            dbconn.update_user_info(user_info)
            logging.info("[acivation] update user info in db | user_info: " + str(user_info))

            bot.send_message(user_info['tg_chat_id'], "Оплата прошла успешна. Активирован 1ый уровень.")        
            logging.info("[acivation] send message than successfull activation | chat_id: " + str(user_info['tg_chat_id']))

            seller = dbconn.get_user_info_by_id(user_info['seller_1_id'])              
            logging.info("[acivation] get seller info by id | id: " + str(user_info['seller_1_id']))

            create_response = paypal.CreatePayouts().create_payouts(seller['paypal'], config.LVL_1_AMOUNT, False)
            logging.info("[acivation] create payouts | seller_paypal: " + str(seller['paypal']) + " | amount: " + str(config.LVL_1_AMOUNT))

            if create_response.status_code == 201:
                batch_id = create_response.result.batch_header.payout_batch_id
                print('Retrieving Payouts batch with id: ' + batch_id)
                get_response = paypal.GetPayouts().get_payouts(batch_id, False)
                logging.info("[acivation] get payouts | batch_id: " + str(batch_id))

                if get_response.status_code == 200:
                    item_id = get_response.result.items[0].payout_item_id
                    print('Retrieving Payout item with id: ' + item_id)
                    get_item_response = paypal.GetPayoutItem().get_payout_item(item_id, False)
                    logging.info("[acivation] get payout item | item_id: " + str(item_id))
                    if get_item_response.status_code == 200:
                        print('Check Payouts status to see if it has completed processing all payments')
                        for i in range(5):
                            time.sleep(2)
                            get_response = paypal.GetPayouts().get_payouts(batch_id, False)
                            if get_response.result.batch_header.batch_status == "SUCCESS":
                                print("Payout success")         
                                access = True                                    

                                break
                        if i == 4:
                            print('Payouts batch is not processed yet')

                        if access:
                            logging.info("[acivation] payout success | batch_id: " + str(batch_id))

                            access = False
                            seller['key_gen'] = int(seller['key_gen']) + 1

                            dbconn.update_user_info(seller)
                            logging.info("[acivation] update seller info in db | seller_info: " + str(seller))

                            if user_info['tg_user_name'] is None:
                                bot.send_message(seller['tg_chat_id'], "Пользователь " + user_info['tg_user_id'] + " приобрёл ключ 1ого уровня за " + str(config.LVL_1_AMOUNT) + "$")
                                logging.info("[acivation] send message to seller that user payed activation | chat_id: " + str(seller['tg_chat_id'] + " | user_tg_id: " + str(user_info['tg_user_id'])))
                            else:
                                bot.send_message(seller['tg_chat_id'], "Пользователь " + user_info['tg_user_name'] + " приобрёл ключ 1ого уровня за " + str(config.LVL_1_AMOUNT) + "$")                                
                                logging.info("[acivation] send message to seller that user payed activation | chat_id: " + str(seller['tg_chat_id']))

                        return "Перейдите в telegram"
                else:
                    print('Failed to retrieve Payouts batch with id: ' + batch_id)
            else:
                print('Failed to create Payouts batch')        
        else:
            print("Link is unreachable")

    except IOError as ioe:
        if isinstance(ioe, HttpError):
            error_json = json.loads(ioe.message)
            issue = error_json['details'][0]['issue']
            description = error_json['details'][0]['description']
            text = ""

            if issue == "MAX_NUMBER_OF_PAYMENT_ATTEMPTS_EXCEEDED":
                text = "Paypal issue:\n" + "issue: " + issue + "\ndescription: " + description
        
            return text

def upgrade(lvl, key, token): 
    try:
        response = paypal.AuthorizeOrder().authorize_order(token, debug=False)
        logging.info("[upgrade] auth order | token: " + str(token))

        if response.status_code == 201:        

            authorization_id = response.result.purchase_units[0].payments.authorizations[0].id
            message_text_user_info = ""
            message_text_seller = ""
            amount = ""
            access = False

            user_info = dbconn.get_user_info(key)
            logging.info("[upgrade] get user info by keu from db | key: " + str(key))
            seller = dbconn.get_user_info_by_id(user_info['seller_' + str(lvl) + '_id'])
            logging.info("[upgrade] get seller info by id | id: " + str(id))
            seller_paypal = seller['paypal']
            
            if lvl == 2:
                amount = config.LVL_2_AMOUNT
                message_text_user_info = "Оплата прошла успешна. Активирован 2ой уровень."
            
            if lvl == 3:
                amount = config.LVL_3_AMOUNT
                message_text_user_info = "Оплата прошла успешна. Активирован 3ий уровень."

            if lvl == 4:
                amount = config.LVL_4_AMOUNT
                message_text_user_info = "Оплата прошла успешна. Активирован 4ый уровень."


            if int(seller['lvl']) <= int(user_info['lvl']):
                seller_paypal = config.ADMINE_PAYPAL
            else:
                if (int(seller['lvl']) == 2 and int(seller['key_gen']) == 8) or (int(seller['lvl']) == 3 and int(seller['key_gen']) == 33):
                    seller_paypal = config.ADMINE_PAYPAL
                    bot.send_message(seller['tg_chat_id'], "Пользователь хотел преобрести у Вас ключ, но Вы достигли лимита генераций ключей, повысте уровень при помощи команды /upgrade")        
                    logging.info("[upgrade] send message that user whant to buy key from seller but seller has max key gen count | chat_id: " + str(seller['tg_chat_id']))
                else:
                    if user_info['tg_user_name'] is None:
                        message_text_seller = "Пользователь " + user_info['tg_user_id'] + " приобрёл ключ " + str(lvl) + " уровня за " + amount + "$"
                    else:
                        message_text_seller = "Пользователь " + user_info['tg_user_name'] + " приобрёл ключ " + str(lvl) + " уровня за " + amount + "$"

                    bot.send_message(seller['tg_chat_id'], message_text_seller)
                    logging.info("[upgrade] send message to seller that user | chat_id: " + str(seller['tg_chat_id']))

                    seller['key_gen'] = int(seller['key_gen']) + 1

                    dbconn.update_user_info(seller)
                    logging.info("[upgrade] update seller info in db | seller_info: " + str(seller))

                    if (int(seller['lvl']) == 2 and int(seller['key_gen']) == 8) or (int(seller['lvl']) == 3 and int(seller['key_gen']) == 33):
                        bot.send_message(seller['tg_chat_id'], "Вы достигли лимита генераций ключей на текухем уровне, повысте уровень при помощи команды /upgrade")        
                        logging.info("[upgrade] send message to seller that he reach max count key gen on his lvl | chat_id: " + str(seller['tg_chat_id']))

            create_response = paypal.CreatePayouts().create_payouts(seller_paypal, amount, False)
            logging.info("[upgrade] create payout | seller_paypal: " + str(seller_paypal) + " | amount: " + str(amount))

            if create_response.status_code == 201:
                batch_id = create_response.result.batch_header.payout_batch_id
                print('Retrieving Payouts batch with id: ' + batch_id)
                get_response = paypal.GetPayouts().get_payouts(batch_id, False)
                logging.info("[upgrade] get payout | batch_id: " + str(batch_id))

                if get_response.status_code == 200:
                    item_id = get_response.result.items[0].payout_item_id
                    print('Retrieving Payout item with id: ' + item_id)
                    get_item_response = paypal.GetPayoutItem().get_payout_item(item_id, False)
                    logging.info("[upgrade] get payout item | item_id: " + str(item_id))

                    if get_item_response.status_code == 200:
                        print('Check Payouts status to see if it has completed processing all payments')
                        for i in range(5):
                            time.sleep(2)
                            get_response = paypal.GetPayouts().get_payouts(batch_id, False)
                            if get_response.result.batch_header.batch_status == "SUCCESS":
                                print("Payout success")          
                                access = True                                

                                break

                        if i == 4:
                            print('Payouts batch is not processed yet')

                        if access:
                            logging.info("[upgrade] payout success | batch_id: " + str(batch_id))

                            access = False
                            user_info['lvl_' + str(lvl) + '_payed'] = 1

                            user_info['lvl'] = lvl
                            user_info['key_gen'] = 0

                            
                            dbconn.update_user_info(user_info)
                            logging.info("[upgrade] update user info in db | user_info: " + str(user_info))

                            bot.send_message(user_info['tg_chat_id'], message_text_user_info)
                            logging.info("[upgrade] send message that successful payment | chat_id: " + str(user_info['tg_chat_id']))

                        return "Перейдите в telegram"
                else:
                    print('Failed to retrieve Payouts batch with id: ' + batch_id)
            else:
                print('Failed to create Payouts batch')        
        else:
            print("Link is unreachable")        

    except IOError as ioe:
        if isinstance(ioe, HttpError):
            error_json = json.loads(ioe.message)
            issue = error_json['details'][0]['issue']
            description = error_json['details'][0]['description']
            text = ""

            text = "Paypal issue:\n" + "issue: " + issue + "\ndescription: " + description
        
            return text
        

async def handle(request):

    try:
        token = request.rel_url.query.get('token', '')
        encrypted_key = request.rel_url.query.get('encrypted_key', '')
        decrypted_data = aes.AESData().decrypt(encrypted_key)

        key = decrypted_data.split()[0]
        action = decrypted_data.split()[1]

        text = "Перейдите обратно в telegram чат"

        if action == ACTIONE_ACTIVATE:
            text = activate(key, token)

        if action == ACTIONE_UPGRADE_LVL_2:
            text = upgrade(2, key, token)

        if action == ACTIONE_UPGRADE_LVL_3:
            text = text = upgrade(3, key, token)

        if action == ACTIONE_UPGRADE_LVL_4:
            text = upgrade(4, key, token)
        
        return web.Response(text=text)

    except:
        pass


try:
    app = web.Application()
    logging.info("define server")

    app.add_routes([web.get('/', handle)])
    logging.info("define routes")

except BaseException as msg:
    logging.error(msg)

if __name__ == '__main__':
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)    
        logging.info("[main] load ssl cert")

        web.run_app(
            app,
            host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=context,
        )

        logging.info("[main] run server")

    except BaseException as msg:
        logging.error(msg)