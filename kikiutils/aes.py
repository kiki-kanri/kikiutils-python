from binascii import a2b_hex
from Cryptodome.Cipher.AES import MODE_CBC, MODE_CFB, MODE_CTR, MODE_ECB, new
from typing import Union

from .hash import md5
from .json import odumps, oloads


class AesCrypt:
    """Padding mode is ZeroPadding."""

    def __init__(
        self,
        key: Union[bytes, str],
        iv: Union[bytes, str] = None,
        mode=MODE_CBC,
        counter=None
    ):
        hashed_key = md5(key, True)

        if mode == MODE_ECB:
            self._get_aes = lambda: new(hashed_key, mode)
        elif mode == MODE_CTR:
            self._get_aes = lambda: new(hashed_key, mode, counter=counter)
        else:
            self._get_aes = lambda: new(hashed_key, mode, iv)

        if mode == MODE_CFB:
            self._pad = self._rstrip = lambda x: x
        else:
            self._pad = lambda x: x + b'\00' * ((16 - (len(x) % 16)) % 16)
            self._rstrip = lambda x: x.rstrip(b'\00')

    @staticmethod
    def _to_bytes(data: Union[bytes, dict, list, str]) -> bytes:
        if isinstance(data, bytes):
            return data

        if isinstance(data, (dict, list)):
            return odumps(data)

        return data.encode('utf-8')

    def decrypt(self, ciphertext: str) -> Union[dict, list, str]:
        ciphertext = a2b_hex(ciphertext.encode('utf-8'))
        text: bytes = self._rstrip(self._get_aes().decrypt(ciphertext))

        try:
            return oloads(text)
        except:
            return text.decode()

    def encrypt(self, text: Union[bytes, dict, list, str]):
        text = self._pad(self._to_bytes(text))
        return self._get_aes().encrypt(text).hex()
