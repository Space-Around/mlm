import config
import sqlite3

def get_user_info(key):
    user_info = {}

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info WHERE key = ?;", (key,))    

    response = cur.fetchone()

    if response is None:
        con.close()
        return False
    else:
        user_info = {
            'id': response[0],
            'key': response[1],
            'tg_chat_id': response[2],
            'tg_user_name': response[3],
            'tg_user_id': response[4],
            'paypal': response[5],
            'email': response[6],
            'lvl': response[7],
            'key_gen': response[8],
            'seller_1_id': response[9],
            'seller_2_id': response[10],
            'seller_3_id': response[11],
            'seller_4_id': response[12],
            'lvl_1_payed': response[13],
            'lvl_2_payed': response[14],
            'lvl_3_payed': response[15],
            'lvl_4_payed': response[16]
        }

    con.close()

    return user_info

def get_user_info_by_id(id):
    user_info = {}

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info WHERE id = ?;", (id,))    

    response = cur.fetchone()

    if response is None:
        con.close()
        return False
    else:
        user_info = {
            'id': response[0],
            'key': response[1],
            'tg_chat_id': response[2],
            'tg_user_name': response[3],
            'tg_user_id': response[4],
            'paypal': response[5],
            'email': response[6],
            'lvl': response[7],
            'key_gen': response[8],
            'seller_1_id': response[9],
            'seller_2_id': response[10],
            'seller_3_id': response[11],
            'seller_4_id': response[12],
            'lvl_1_payed': response[13],
            'lvl_2_payed': response[14],
            'lvl_3_payed': response[15],
            'lvl_4_payed': response[16]
        }

    con.close()

    return user_info

def get_user_info_by_tg_id(tg_id):
    user_info = {}

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info WHERE tg_user_id = ?;", (tg_id,))    

    response = cur.fetchone()

    if response is None:
        con.close()
        return False
    else:
        user_info = {
            'id': response[0],
            'key': response[1],
            'tg_chat_id': response[2],
            'tg_user_name': response[3],
            'tg_user_id': response[4],
            'paypal': response[5],
            'email': response[6],
            'lvl': response[7],
            'key_gen': response[8],
            'seller_1_id': response[9],
            'seller_2_id': response[10],
            'seller_3_id': response[11],
            'seller_4_id': response[12],
            'lvl_1_payed': response[13],
            'lvl_2_payed': response[14],
            'lvl_3_payed': response[15],
            'lvl_4_payed': response[16]
        }

    con.close()

    return user_info

def get_user_info_by_key(key):
    user_info = {}

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info WHERE key = ?;", (key,))    

    response = cur.fetchone()

    if response is None:
        con.close()
        return False
    else:
        user_info = {
            'id': response[0],
            'key': response[1],
            'tg_chat_id': response[2],
            'tg_user_name': response[3],
            'tg_user_id': response[4],
            'paypal': response[5],
            'email': response[6],
            'lvl': response[7],
            'key_gen': response[8],
            'seller_1_id': response[9],
            'seller_2_id': response[10],
            'seller_3_id': response[11],
            'seller_4_id': response[12],
            'lvl_1_payed': response[13],
            'lvl_2_payed': response[14],
            'lvl_3_payed': response[15],
            'lvl_4_payed': response[16]
        }

    con.close()

    return user_info

def update_user_info(user_info):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("UPDATE user_info SET tg_chat_id = ?, tg_user_name = ?, tg_user_id = ?, paypal = ?, email = ?, lvl = ?, key_gen = ?, seller_1_id = ?, seller_2_id = ?, seller_3_id = ?, seller_4_id = ?, lvl_1_payed = ?, lvl_2_payed = ?, lvl_3_payed = ?, lvl_4_payed = ?  WHERE key = ?;", (user_info['tg_chat_id'], user_info['tg_user_name'], user_info['tg_user_id'], user_info['paypal'], user_info['email'], user_info['lvl'], user_info['key_gen'], user_info['seller_1_id'], user_info['seller_2_id'], user_info['seller_3_id'], user_info['seller_4_id'], user_info['lvl_1_payed'], user_info['lvl_2_payed'], user_info['lvl_3_payed'], user_info['lvl_4_payed'], user_info['key']))    
    con.commit()
    con.close()

    return user_info

def insert_user_info(user_info):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO user_info (key, tg_chat_id, tg_user_name, tg_user_id, paypal, email, lvl, key_gen, seller_1_id, seller_2_id, seller_3_id, seller_4_id, lvl_1_payed, lvl_2_payed, lvl_3_payed, lvl_4_payed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_info['key'], user_info['tg_chat_id'], user_info['tg_user_name'], user_info['tg_user_id'], user_info['paypal'], user_info['email'], user_info['lvl'], user_info['key_gen'], user_info['seller_1_id'], user_info['seller_2_id'], user_info['seller_3_id'], user_info['seller_4_id'], user_info['lvl_1_payed'], user_info['lvl_2_payed'], user_info['lvl_3_payed'], user_info['lvl_4_payed']))    
    con.commit()
    con.close()

def check_key(key):
    access = False

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info WHERE key = ?;", (key,))

    if cur.fetchone() is None:
        access = False
    else:
        access = True
        
    con.close()

    return access

def check_tg_user_id(tg_user_id):
    access = False

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_info WHERE tg_user_id = ?;", (tg_user_id,))

    if cur.fetchone() is None:
        access = False
    else:
        access = True
        
    con.close()

    return access
    
# print(get_user_info_by_id(1))