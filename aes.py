from Crypto.Cipher import AES
import config
import json

def decrypt(data):    
    if (data[0:4] == config.DATA_DETECTION):
        key = config.DATA_KEY        
        nonce = bytes.fromhex(data[4:36])

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(bytes.fromhex(data[36:len(data)]))
        
        return plaintext.decode("utf-8")
    else:
        return False

def encrypt(data):
    key = config.DATA_KEY
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce    
    
    data_strigify = data.encode('utf-8')

    ciphertext, tag = cipher.encrypt_and_digest(data_strigify)

    data_key = config.DATA_DETECTION + str(nonce.hex()) + str(ciphertext.hex())

    return data_key