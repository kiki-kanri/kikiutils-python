import aiohttp
import asyncio
import re
import requests
import time

from random import randint, shuffle
from requests import Response
from .aes import AesCrypt
from .check import isdict
from .log import logger
from .requests import get_response_content_type
from .string import random_str
from .uuid import get_uuid


class DataTransmission:
    def __init__(
        self,
        key: bytes | str,
        iv: bytes | str,
        api_base_url: str = ''
    ):
        self.api_base_url = api_base_url
        self.iv = iv
        self.key = key
        self.session = aiohttp.ClientSession()

    async def async_request(
        self,
        url: str,
        data: dict,
        method: str = 'post',
        data_add_uuid: bool = False,
        **kwargs
    ):
        request_kwargs = self.get_request_kwargs(
            url,
            data,
            method,
            data_add_uuid,
            **kwargs
        )

        async with self.session.request(**request_kwargs) as response:
            if self.response_is_text(response):
                return self.process_hash_data(await response.text())

            return await response.content.read()

    def get_request_kwargs(
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
        request_data = {
            random_str(randint(4, 8), randint(9, 128)): hash_data
        }

        request_kwargs = {
            'method': method,
            'url': url,
            **kwargs
        }

        if kwargs.get('files'):
            request_kwargs['data'] = request_data
        else:
            request_kwargs['json'] = request_data

        return request_kwargs

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
        aes = AesCrypt(self.key, self.iv)
        hash_data = aes.encrypt(data_list)
        return hash_data

    def process_hash_data(self, hash_text: str) -> dict:
        aes = AesCrypt(self.key, self.iv)
        data = {}

        try:
            for item in aes.decrypt(hash_text):
                data[item[0]] = item[1]

            return data
        except:
            pass

    def request(
        self,
        url: str,
        data: dict = {},
        method: str = 'post',
        data_add_uuid: bool = False,
        **kwargs
    ):
        request_kwargs = self.get_request_kwargs(
            url,
            data,
            method,
            data_add_uuid,
            **kwargs
        )

        response = requests.request(**request_kwargs)

        if self.response_is_text(response):
            return self.process_hash_data(response.text)

        return response.content

    def response_is_text(
        self,
        response: aiohttp.ClientResponse | Response
    ):
        return get_response_content_type(response) == 'text/plain'


class DataTransmissionSecret:
    aes: AesCrypt
    data_transmission: DataTransmission

    @classmethod
    async def async_request(
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
                response_data = await cls.data_transmission.async_request(
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

            result = cls.check_response_data(
                response_data,
                error_log,
                wait_success
            )

            if result == 'break':
                return
            elif result:
                return result

            await asyncio.sleep(1)

    @staticmethod
    def check_response_data(
        response_data: bytes | dict,
        error_log: bool,
        wait_success: bool
    ):
        if (
            isdict(response_data)
            and response_data.get('success')
            or not isdict(response_data)
        ):
            return response_data

        if error_log:
            logger.error('Get data error！')

        if not wait_success:
            return 'break'

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
    def request(
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
                response_data = cls.data_transmission.request(
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

            result = cls.check_response_data(
                response_data,
                error_log,
                wait_success
            )

            if result == 'break':
                return
            elif result:
                return result

            time.sleep(1)
