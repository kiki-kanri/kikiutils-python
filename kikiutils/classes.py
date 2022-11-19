import re
import requests
import time

from random import randint, shuffle

from .aes import AesCrypt
from .check import isdict
from .log import logger
from .requests import get_response_content_type
from .string import random_str
from .uuid import get_uuid


class DataTransmission:
    def __init__(
        self,
        iv: bytes | str,
        key: bytes | str,
        api_base_url: str = ''
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

        for item in aes.decrypt(hash_data):
            data[item[0]] = item[1]

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
            url,
            data={
                random_str(randint(4, 8), randint(9, 128)): hash_data
            },
            **kwargs
        )

        content_type = get_response_content_type(response)

        if content_type == 'text/html':
            return self.process_hash_data(response.text)

        return response


class DataTransmissionSecret:
    aes: AesCrypt
    data_transmission: DataTransmission

    @classmethod
    def hash_data(cls, data: dict):
        return cls.data_transmission.hash_data(data)

    @classmethod
    def process_hash_data(cls, hash_data: str):
        try:
            return cls.data_transmission.process_hash_data(
                hash_data
            )
        except:
            pass

    @classmethod
    def requests(
        cls,
        url: str,
        data: dict = {},
        method: str = 'post',
        wait_success: bool = True,
        error_log: bool = True,
        **kwargs
    ):
        while True:
            try:
                response_data = cls.data_transmission.requests(
                    url,
                    data,
                    method,
                    **kwargs
                )
            except Exception as error:
                if error_log:
                    logger.error(f'Get data request error：{error}')

                if wait_success:
                    continue

            if (
                isdict(response_data)
                and response_data.get('success')
                or not isdict(response_data)
            ):
                return response_data

            if error_log:
                logger.error('Get data error！')

            if not wait_success:
                return None

            time.sleep(1)
