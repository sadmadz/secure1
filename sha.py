import hashlib


class SHA:
    def __init__(self, data):
        self.data = data

    def encrypt(self, param):
        result = ''
        if int(param) == 256:
            result = hashlib.sha256(self.data.encode())
        if int(param) == 384:
            result = hashlib.sha384(self.data.encode())
        if int(param) == 224:
            result = hashlib.sha224(self.data.encode())
        if int(param) == 512:
            result = hashlib.sha512(self.data.encode())
        if int(param) == 1:
            result = hashlib.sha1(self.data.encode())
        else:
            result = hashlib.sha256(self.data.encode())
        f = open('sha.txt', 'w')
        f.write(result.hexdigest())
        f.close()
        print(f"SHA{int(param)} cipher :  {result.hexdigest()}")
