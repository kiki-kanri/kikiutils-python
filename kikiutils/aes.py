from binascii import a2b_hex, b2a_hex
from Cryptodome.Cipher import AES
from typing import Union

from .check import isdict, islist
from .string import b2s, s2b
from .hash import md5
from .json import odumps, oloads


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

    def pad(self, data: Union[bytes, dict, list, str]) -> bytes:
        if isdict(data) or islist(data):
            data = odumps(data)

        data = s2b(data)

        if len(data) % 16:
            data += b' ' * (16 - (len(data) % 16))

        return data

    def encrypt(self, text: Union[dict, list, str]):
        text = self.pad(text)
        ciphertext = self.cipher.encrypt(text)
        return b2s(b2a_hex(ciphertext))

    def decrypt(self, ciphertext: str) -> Union[dict, list, str]:
        ciphertext = a2b_hex(s2b(ciphertext))
        text = self.cipher.decrypt(ciphertext).rstrip()

        try:
            return oloads(text)
        except:
            return b2s(text)
