# from Crypto.Cipher import AES

# key = b'Sixteen byte key'
# # cipher = AES.new(key, AES.MODE_EAX)
# # nonce = cipher.nonce
# # print(nonce.hex())
# # data = "Hello World!".encode('utf-8')

# # ciphertext, tag = cipher.encrypt_and_digest(data)

# nonce = bytes.fromhex('2ca60debd6b1f99a535997710c25b65a')
# ciphertext = bytes.fromhex('bf362fc1e6c7ef5c07953b72')

# cipher2 = AES.new(key, AES.MODE_EAX, nonce=nonce)
# plaintext = cipher2.decrypt(ciphertext)

# # print(ciphertext.hex())
# print(plaintext.decode("utf-8"))
# import datetime
# from dateutil.parser import parse

# print(parse("2021-04-19 01:13:35.838272") + datetime.timedelta(45))

# def gen(cmd_param):
#     paypal_account = ""
#     email_account = ""

#     for i in range(0, len(cmd_param)):
#         if cmd_param != '\n':
#             paypal_account = paypal_account + str(cmd_param[i])
#         else:
#             break

#     for i in range(len(cmd_param) - len(paypal_account), len(cmd_param)):
#         if cmd_param != '\n':
#             email_account = email_account + str(cmd_param[i])
#         else:
#             break

#     print("PayPal: " + paypal_account)
#     print("Email: " + email_account)

param = """paypal@example.com email@example.com"""

print(param.split()[0])