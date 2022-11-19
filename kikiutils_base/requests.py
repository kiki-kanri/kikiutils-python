import aiohttp
import requests

from typing import Union


def get_response_content_type(
    response: Union[aiohttp.ClientResponse, requests.Response]
):
    for key, value in response.headers.items():
        if key.lower() == 'content-type':
            return value.split(';')[0].strip()
