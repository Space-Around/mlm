import sqlite3
import config

con = sqlite3.connect(config.DB_NAME, check_same_thread=False)
cur = con.cursor()

cur.execute("SELECT * FROM user_info")

response = cur.fetchall()

if response is None:
    pass
else:
    for i in range(0, len(response)):
        print("-----------------------------------------------")
        info = ""

        for j in range(0, 17):
            info = info + str(response[i][j]) + "|"

        print(info)