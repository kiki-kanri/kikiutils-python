import json

from binascii import a2b_hex, b2a_hex
from Cryptodome.Cipher import AES
from typing import Union

from .check import isdict, islist
from .string import b2s, s2b
from .hash import md5


class AesCrypt:
    def __init__(
        self,
        key: Union[bytes, str],
        iv: Union[bytes, str] = None,
        mode=AES.MODE_CBC
    ):
        iv = s2b(iv)
        key = md5(key, True)

        if mode == AES.MODE_ECB:
            self.cipher = AES.new(key, mode)
        else:
            self.cipher = AES.new(key, mode, iv=iv)

    def pad(self, text: Union[dict, list, str]):
        if isdict(text) or islist(text):
            text = json.dumps(text)

        text = s2b(text)

        while len(text) % 16 != 0:
            text += b' '

        return text

    def encrypt(self, text: Union[dict, list, str]):
        text = self.pad(text)
        ciphertext = self.cipher.encrypt(text)
        return b2s(b2a_hex(ciphertext))

    def decrypt(self, ciphertext: str):
        ciphertext = a2b_hex(s2b(ciphertext))
        text = self.cipher.decrypt(ciphertext)

        try:
            text = b2s(text).rstrip()

            try:
                data = json.loads(text)
                return data
            except:
                return text
        except:
            return text.rstrip()
