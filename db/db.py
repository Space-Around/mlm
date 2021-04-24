import config
import sqlite3

class DBConnection() :

    def __init__(self):
        self.con = sqlite3.connect(config.DB_NAME, check_same_thread=False)
        self.cur = self.con.cursor()

        print("Database start connection")

    def get_user_info(self, key):
        user_info = {}

        self.cur.execute("SELECT * FROM user_info WHERE key = ?;", (key,))    

        response = self.cur.fetchone()

        if response is None:
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

        return user_info


    def get_user_info_by_id(self, id):
        user_info = {}

        self.cur.execute("SELECT * FROM user_info WHERE id = ?;", (id,))    

        response = self.cur.fetchone()

        if response is None:
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

        return user_info


    def get_user_info_by_tg_id(self, tg_id):
        user_info = {}

        self.cur.execute("SELECT * FROM user_info WHERE tg_user_id = ?;", (tg_id,))    

        response = self.cur.fetchone()

        if response is None:
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

        return user_info


    def get_user_info_by_key(self, key):
        user_info = {}

        self.cur.execute("SELECT * FROM user_info WHERE key = ?;", (key,))    

        response = self.cur.fetchone()

        if response is None:
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

        return user_info


    def update_user_info(self, user_info):
        self.cur.execute("UPDATE user_info SET tg_chat_id = ?, tg_user_name = ?, tg_user_id = ?, paypal = ?, email = ?, lvl = ?, key_gen = ?, seller_1_id = ?, seller_2_id = ?, seller_3_id = ?, seller_4_id = ?, lvl_1_payed = ?, lvl_2_payed = ?, lvl_3_payed = ?, lvl_4_payed = ?  WHERE key = ?;", (user_info['tg_chat_id'], user_info['tg_user_name'], user_info['tg_user_id'], user_info['paypal'], user_info['email'], user_info['lvl'], user_info['key_gen'], user_info['seller_1_id'], user_info['seller_2_id'], user_info['seller_3_id'], user_info['seller_4_id'], user_info['lvl_1_payed'], user_info['lvl_2_payed'], user_info['lvl_3_payed'], user_info['lvl_4_payed'], user_info['key']))    
        self.con.commit()


    def insert_user_info(self, user_info):
        self.cur.execute("INSERT INTO user_info (key, tg_chat_id, tg_user_name, tg_user_id, paypal, email, lvl, key_gen, seller_1_id, seller_2_id, seller_3_id, seller_4_id, lvl_1_payed, lvl_2_payed, lvl_3_payed, lvl_4_payed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_info['key'], user_info['tg_chat_id'], user_info['tg_user_name'], user_info['tg_user_id'], user_info['paypal'], user_info['email'], user_info['lvl'], user_info['key_gen'], user_info['seller_1_id'], user_info['seller_2_id'], user_info['seller_3_id'], user_info['seller_4_id'], user_info['lvl_1_payed'], user_info['lvl_2_payed'], user_info['lvl_3_payed'], user_info['lvl_4_payed']))    
        self.con.commit()


    def check_key(self, key):
        access = False

        self.cur.execute("SELECT * FROM user_info WHERE key = ?;", (key,))

        if self.cur.fetchone() is None:
            access = False
        else:
            access = True

        return access


    def check_tg_user_id(self, tg_user_id):
        access = False

        self.cur.execute("SELECT * FROM user_info WHERE tg_user_id = ?;", (tg_user_id,))

        if self.cur.fetchone() is None:
            access = False
        else:
            access = True

        return access