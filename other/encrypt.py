
from Crypto.Cipher import AES
from Crypto import Random


class Encrypt(object):
    def __init__(self, password):
        self.password = self.add_to_16(password).encode("utf-8")

    def add_to_16(self, text):
        while len(text) % 16 != 0:
            text += '\0'
        return (text)

    def encrypt(self, data):
        bs = AES.block_size
        pad = lambda s: s + (bs - len(s) % bs) * bytes([bs - len(s) % bs])
        iv = Random.new().read(bs)
        cipher = AES.new(self.password, AES.MODE_CBC, iv)
        data = cipher.encrypt(pad(data))
        data = iv + data
        return (data)

    def decrypt(self, data):
        bs = AES.block_size
        if len(data) <= bs:
            return (data)
        unpad = lambda s : s[0:-(s[-1])]
        iv = data[:bs]
        cipher = AES.new(self.password, AES.MODE_CBC, iv)
        data  = unpad(cipher.decrypt(data[bs:]))
        return (data)
