from Crypto.Cipher import AES

from pymt5pure.helpers import hash_password_vrand

ENCRYPT_IV = 2
DECRYPT_IV = 3


class MT5AES(object):
    def __init__(self, password: str, crypt_rand: str):
        self.crypt_iv = list(hash_password_vrand(password, crypt_rand))
        self.cipher = AES.new(
            key=self.crypt_iv[0] + self.crypt_iv[1],
            mode=AES.MODE_ECB,
        )

    def _encrypt(self, data, iv):
        key = 16
        for i in range(len(data)):
            if key >= 16:
                # get new key for xor
                self.crypt_iv[iv] = self.cipher.encrypt(self.crypt_iv[iv])
                key = 0

            # xor all bytes
            yield data[i] ^ self.crypt_iv[iv][key]
            key += 1

    def encrypt(self, data):
        return bytes(self._encrypt(data, ENCRYPT_IV))

    def decrypt(self, data):
        return bytes(self._encrypt(data, DECRYPT_IV))
