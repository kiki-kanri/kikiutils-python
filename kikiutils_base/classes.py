import re
import requests

from kikiutils_base.string import random_str
from random import randint, shuffle

from .aes import AesCrypt
from .requests import get_response_content_type
from .uuid import get_uuid


class DataTransmission:
    def __init__(
        self,
        api_base_url: str,
        iv: bytes | str,
        key: bytes | str
    ):
        self.api_base_url = api_base_url
        self.iv = iv
        self.key = key

    def hash_data(self, data: dict):
        for _ in range(1, randint(randint(2, 5), randint(6, 16))):
            data[random_str(randint(8, 16), randint(17, 256))] = random_str(
                randint(8, 32),
                randint(33, 512)
            )

        data_list = []

        for key, value in data.items():
            data_list.append([key, value])

        shuffle(data_list)
        aes = AesCrypt(self.iv, self.key)
        hash_data = aes.encrypt(data_list)
        return hash_data

    def process_hash_data(self, hash_data: str) -> dict:
        aes = AesCrypt(self.iv, self.key)
        data = {}

        try:
            for item in aes.decrypt(hash_data):
                data[item[0]] = item[1]
        except:
            pass

        return data

    def requests(
        self,
        url: str,
        data: dict,
        method: str = 'post',
        data_add_uuid: bool = False,
        **kwargs
    ):
        if not re.match(r'https?:\/\/', url):
            url = f'{self.api_base_url}{url}'

        if data_add_uuid:
            data['uuid'] = get_uuid()

        hash_data = self.hash_data(data)

        response = requests.request(
            method,
            f'{self.api_base_url}{url}',
            data={
                random_str(randint(4, 8), randint(9, 128)): hash_data
            },
            **kwargs
        )

        content_type = get_response_content_type(response)

        if content_type == 'text/html':
            return self.process_hash_data(response.text)

        return response
