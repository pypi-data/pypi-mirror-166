from Crypto.Cipher import AES
import json
import base64
from itsdangerous import base64_encode
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64 
#auth sandeshrathod09@gmail.com
class RijndaelEncryptor(object):
    def __init__(self, k=16):
        self.k = k
    def _pkcs7decode(self, text):
        val = text[-1]
        if val > self.k:
            raise ValueError('Input is not padded or padding is corrupt')
        l = len(text) - val
        return (text[:l]).decode(encoding="UTF-8")

    def _pkcs7encode(self, text):
        l = len(text)
        val = self.k - (l % self.k)        
        return text + bytes([val] * val)
 
    def encrypt(self, text, input_key, input_iv):
        key = bytes(input_key,'utf-8')
        iv = bytes(input_iv,'utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(text, AES.block_size))
        ct =base64.b64encode(ct_bytes).decode('utf-8')
        result = json.dumps(ct)
        return result
 
    def decrypt(self, text, input_key, input_iv=None):
        key = bytes(input_key, 'ascii')
        iv = bytes(input_iv,'ascii')
        aes = AES.new(key, AES.MODE_CBC,iv)
        decode_text = base64.b64decode(text)
        pad_text = aes.decrypt(decode_text)
        return self._pkcs7decode(pad_text)

class sarthi:

    def __init__(self,key,iv):
        self.key = key
        self.iv = iv
        self.obj = RijndaelEncryptor()

    def encrypt(self,data):
        data=json.dumps(data).encode('utf-8')
        return self.obj.encrypt(data,self.key,self.iv)
    
    def decrypt(self,data):
        return self.obj.decrypt(data,self.key,self.iv)

