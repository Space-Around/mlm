from Crypto.Cipher import AES
import config
import json

def decrypt(data):    
    if (data[0:4] == config.DATA_DETECTION):
        key = config.DATA_KEY        
        nonce = bytes.fromhex(data[4:36])

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(bytes.fromhex(data[36:len(data)]))
        
        return json.loads(plaintext)
    else:
        return False

def encrypt(data):
    key = config.DATA_KEY
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce    
    
    data_strigify = json.dumps(data).encode('utf-8')

    ciphertext, tag = cipher.encrypt_and_digest(data_strigify)

    data_key = config.DATA_DETECTION + str(nonce.hex()) + str(ciphertext.hex())

    return data_key

with open("./test_key_struct.json") as f:
    data_key_new = json.load(f)

# key = encrypt(data_key_new)
# print(key)
key = "hRpO31526f05f8cdc2a133c6789d92e68435cd35295e6b98cfe9ef98a2ccf30b3ea82e9d1811fee2a1f67885197f8e855e8abce9cf36c2848bcf6573243ed0e7b6695d58ec7580918d7e5ab75ce010007e1dbcb44b88db0e203328f26e35fd6ed3dfda2a979e44ac024323000b6e4ee3c250c71112b02be411fd712736f4adf30cea8b2a6eb55986110c9ddf711c63b198014de19cb4f2a493c1d727a0a218546d605b7fb112daca896e511b331c4fd1794920d2e264256e88e827ff2124b722fb15dd464c7ff54a4261620dc8c9c90598bf854b9ec3c2a039279f0e59aeebcc11298689b597ff60a5edeb3defb5e2abdaaa9d51a9ae88d03ff0df927e905db2f8dcbfb190e93aa2eb47b9ed56bdea6f88a0fb01362884238bddab0989bf9778dda08a6d68fe737712f9580110ee3e4e420ad430dfd7b8f39ad564009b6a802ad1694d86ae87a4cbd9834b795428d3713653a472602782131c079d8fb26ae6145418bf30539b34d40864a7c2ad7cac8119f770b678df1d221e310e31bbbf22fbdef5764e9a3cf5b25b629548be3d0674a0ff8c7150981c82417902415ae478c60104c98ddb9d25b9196107996e7732da8044eac7026450e60a8815fea551e69d401a8a11c27d76768de09da9c4782201e000afb320ce46c8728248260ba07c87e0ac5e6b2fc6474b696a9b3e48a41d890801a8db8b0edc45dd248dab558da2cadab4c0f11f1b15ccde7b4f7a71f6082bf368b442e111a842f54b60943bfcbc387866f51f4ab98603db826789b132f0a52a5313eabccbe1f9083cc2bdc9f69462267f285ed86155b5a11f277b45d91982e3e140b246a03179a7ed3a258f6f712f8b0da006aa51a97d54e3b86f00f91619a282cfc9825d71332ec53345177111994c7dfa3f029a8db57057113c894ad99d4c477708cc1e3d4d608d1c8e8564dcefb1404b66c0c7099e7f412d879bcce1f2d0fd04a4c38ededdcadfa501864a3e56abf9b4275fd0f6bb75b753d8eb4bd137f80a1296a41abd0961ea64e29993e04bd485e0b7cfa3a09b1dfb9629361d3d1d6d0ca15160b35e72b9b7b4688469ae28e1c4c4babbc8abd482298fc07014c89c31eedf26029dd4726e16e5340cb35eaccc7c6282613701e830a27a8ffa29c00544cff6ac5ed1821d93f754827292617b594e338483df36dbc6498d87b7c497ee0a8542e9dbc66c12b3202f9601706d4411c4bed43532c7106c4893107b1c35c803ac8f52c356d478f5806e72cdb5a93fb78876f6e283578dc15611fec501e3a8ba5bb39e56eb036b6c93b65e4453ae5906c1ff0247b11fa411ba8747b7b37e63fac921fa668c3a361be1a8bf96409deefc8ae03f388a9903e5c5bbb2b3dff08f726d406fe30a5c25861f93aad6f12d82ad2da646f0e44f83a72a8aaf7dd889bfbc683d13a0415cd83e908ec97064c6efc96daa733f5b2b3efe1586e1ff1dfa11b41216cf32286bc76a97f42c408092d27832321bd485"

print(decrypt(key))