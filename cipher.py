import base64
import binascii
import hashlib
import random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

from sha import SHA


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'


def write_to_file(filename, data):
    file = open(f'{filename}.txt', 'w')
    file.write(data)


def get_data(filename):
    file = open(f'{filename}.txt', 'r')
    return file.read()


data = get_data('data')


class AESCipher(object):

    def __init__(self, key):
        try:
            f = open('aes_key.txt', 'rb')
        except:
            self.bs = AES.block_size
            self.key = hashlib.sha256(key.encode()).digest()
            f = open('aes_key.txt', 'wb')
            f.write(self.key)
            f.close()

    def encrypt(self, raw):
        f = open('aes_key.txt', 'rb')
        key = f.read()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        f = open('aes_key.txt', 'rb')
        key = f.read()
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.decrypt(enc[AES.block_size:]).decode()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class RSACipher(object):
    def __init__(self):
        try:
            f = open('rsa.pem', 'rb')
        except:
            key = RSA.generate(1024)
            f = open('rsa.pem', 'wb')
            f.write(key.exportKey('PEM'))
            f.close()

    def enc(self):
        f = open('rsa.pem', 'rb')
        pkey = RSA.importKey(f.read()).publickey()
        encryptor = PKCS1_OAEP.new(pkey)
        self.encrypted = encryptor.encrypt(data.encode())
        f = open('rsa.txt', 'w')
        f.write(binascii.hexlify(self.encrypted).decode("utf-8"))
        f.close()
        print("Encrypted:", binascii.hexlify(self.encrypted).decode("utf-8")+"=")

    def dec(self):
        f = open('rsa.pem', 'rb')
        prkey = RSA.importKey(f.read())
        decryptor = PKCS1_OAEP.new(prkey)
        decrypted = decryptor.decrypt(self.encrypted)
        print('Decrypted:', decrypted.decode("utf-8"))


while True:
    print(f'{bcolors.HEADER}Enter cipher method: ')
    query = input()
    query = query.replace(" ", "")
    if query == 'quit':
        break
    if query == 'aes':
        try:
            test2 = AESCipher(str(random.getrandbits(128)))
            enc = test2.encrypt(str(data))
            dec = test2.decrypt(bytes(enc))
            f = open('aes.txt', 'w')
            f.write(enc.decode("utf-8"))
            f.close()
            print("Encrypted:", enc.decode("utf-8"))
            print("Decrypted:", dec)
        except Exception as e:
            print(e)
            print(f"{bcolors.FAIL}Wrong query")
    elif query == 'rsa':

        try:
            test = RSACipher()
            test.enc()
            test.dec()
        except Exception as e:
            print(e)
            print(f"{bcolors.FAIL}Wrong query")
    elif query.__contains__('sha'):
        try:
            param = query.split('-')[1]
            SHA(data).encrypt(param)
        except Exception as e:
            print(e)
            print(f"{bcolors.FAIL}Wrong query")
    else:
        print(f"{bcolors.FAIL}Wrong query")
