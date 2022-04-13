import copy as _copy
import datetime as _datetime
import io as _io
import json as _json
import magic as _magic
import os as _os
import random as _random
import re as _re
import requests as _requests
import shutil as _shutil
import string as _string
import time as _time
import urllib3 as _urllib3

from PIL import Image as _Image
from pyclbr import Function as _Function
from typing import Any as _Any


_Image.MAX_IMAGE_PIXELS = None
_urllib3.disable_warnings()


TYPE_INT = type(int())
TYPE_STR = type(str())
TYPE_BYTES = type(bytes())


# Array


# Check

def check_domain(domain: str):
    """檢查域名是否能通過ping測試
    """

    domain = _re.sub(r'[;|&\-\s​]', '', domain)
    return not _os.system(f'ping -c 1 -s 8 {domain}') # 若正常ping返回數值0


def check_email(email: str):
    """檢查信箱格式是否正常且＠後域名能通過測試
    """

    if _re.match(r'.*[+\-*/\\;&|\s​].*', email): return False
    return check_domain(email.split('@')[-1])


def check_file_type(file: bytes | _io.BytesIO | _io.FileIO, allow_types: set, file_mime: list = None):
    """檢查檔案類型是否在允許清單
    """

    if not file_mime: file_mime = get_file_mime(file)
    return file_mime[0] in allow_types


def check_file_ext(file: bytes | _io.BytesIO | _io.FileIO, allow_exts: set, file_mime: list = None):
    """檢查檔案副檔名是否在允許清單
    """

    if not file_mime: file_mime = get_file_mime(file)
    return file_mime[1] in allow_exts


def isint_or_digit(text: int | str):
    """檢查值是否為數字或是字串型態的數字
    """

    return is_int(text) or (is_str(text) and text.isdigit())


def is_bytes(*args):
    """判斷是否為bytes
    """

    return all([type(arg) == TYPE_BYTES for arg in args])


def is_int(*args):
    """判斷是否為int
    """

    return all([type(arg) == TYPE_INT for arg in args])


def is_str(*args):
    """判斷是否為str
    """

    return all([type(arg) == TYPE_STR for arg in args])


def response_is_ok(response: _requests.Response, only_html: bool = True) -> bool:
    """檢查該response是否正常回應
    """

    return response and 200 <= response.status_code < 300 and \
        (not only_html or 'text/html' in response.headers['Content-Type'])


# File

def create_dir(path: str):
    """建立資料夾
    """

    try:
        _os.makedirs(path)
        return True
    except:
        return False


def remove_dir(path: str):
    """刪除資料夾
    """

    try:
        _shutil.rmtree(path)
        return True
    except:
        return False


def save_file(file: bytes | _io.BytesIO | _io.FileIO, path: str, replace: bool = True):
    """儲存檔案
    """

    try:
        if _os.path.exists(path) and not replace: raise FileExistsError()
        if getattr(file, 'read', None): file = file.read()
        with open(path, 'wb') as f: f.write(file)
        return True
    except:
        return False


def save_file_as_bytesio(
    save_fnc: _Function,
    get_bytes: bool = False,
    **args
):
    """將檔案儲存成io.BytesIO

    Args:
        save_fnc: 儲存檔案的Function
        get_bytes: 是否返回bytes
    """

    with _io.BytesIO() as output:
        save_fnc(output, **args)
        file_bytes = output.getvalue()

    if get_bytes: return file_bytes
    return _io.BytesIO(file_bytes)


def move_file(path: str, target_path: str):
    """移動檔案或資料夾
    """

    try:
        _shutil.move(path, target_path)
        return True
    except:
        return False


def rename(path: str, name: str):
    """重新命名檔案或資料夾
    """

    try:
        _os.rename(path, name)
        return True
    except:
        return False


def del_file(path: str):
    """刪除檔案
    """

    try:
        _os.remove(path)
        return True
    except:
        return False


# Get

def get_file_mime(file: bytes | _io.BytesIO | _io.FileIO):
    """獲取檔案MIME類別
    """

    file = _copy.deepcopy(file).read(2048) if getattr(file, 'read', None) else file[:2048]
    file_mime = _magic.from_buffer(file, mime = True)
    if file_mime: return file_mime.split('/')


def get_host(url: str):
    """獲取輸入網址的host
    """

    return _re.sub(r'https?:\/\/', '', url).split('/')[0]


def get_int_data(data: str | int, default = None):
    """輸入字串或數字，返回數字，若字串不為純數字，返回default的值(None)
    """

    return int(data) if isint_or_digit(data) else default


def get_requests_headers(
    url: str,
    host:bool = True,
    referer: bool = False
):
    """獲取requests headers
    """

    http = 'http' if 'https://' not in url else 'https://'
    host = get_host(url)

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Ch-Ua-Mobile': '?0',
        'Accept-Encoding': '*',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,af;q=0.6,ja;q=0.5,zh-CN;q=0.4'
    }

    if host: headers['Host'] = host
    if referer: headers['Referer'] = f'{http}://{host}/'
    return headers


def get_response(
    url: str,
    cookies: dict = {},
    headers: bool = True,
    host: bool = True,
    referer: bool = False,
    timeout: int = 3
):
    """獲取網站requests回應
    """

    max_redirect = 5
    redirect_urls = set()

    while max_redirect:
        try:
            args = {
                'url': url,
                'timeout': timeout,
                'allow_redirects': False
            }

            if headers:
                headers = get_requests_headers(url, host, referer)
                args['headers'] = headers

            response = _requests.get(**args)

            if 300 <= response.status_code <= 310:
                redirect_to = response.headers['location']
                if redirect_to in redirect_urls: break
                url = redirect_to
                redirect_urls.add(url)
                max_redirect -= 1
            else:
                break
        except:
            return None

    return response


# Image

def convert_image(
    image_file: bytes | _io.BytesIO | _io.FileIO,
    format: str = 'webp',
    quality: int = 100,
    return_bytes: bool = False
):
    """將圖片轉換為其他格式
    """

    try:
        if is_bytes(image_file): image_file = _io.BytesIO(image_file)
        image = _Image.open(image_file)

        return save_file_as_bytesio(
            image.save,
            return_bytes,
            format = format,
            quality = quality,
            lossless = False
        )
    except:
        return False


def download_image(
    url: str,
    save_path: str,
    max_size: int = 5242880,
    save_format: str = 'webp'
):
    """下載圖片並儲存
    """

    response = get_response(url)

    if response_is_ok(response, False):
        image_bytes = response.content

        if len(image_bytes) <= max_size:
            return save_image(image_bytes, save_path, save_format)

    return False


def save_image(
    image_file: bytes | _io.BytesIO | _io.FileIO,
    save_path: str,
    format: str = 'webp',
    image_mime: list = None
):
    """儲存圖片
    """

    if image_file:
        if getattr(image_file, 'read', None): image_file = image_file.read()
        if not image_mime: image_mime = get_file_mime(image_file)

        if image_mime[0] == 'image':
            if image_mime[1] != format:
                image_file = convert_image(image_file, format, return_bytes = True)

            return save_file(image_file, save_path)

    return False


# String

_RANDOM_LETTERS = _string.ascii_letters + _string.digits

def random_str(min_l: int = 8, max_l: int = 8):
    return ''.join(_random.choice(_RANDOM_LETTERS) \
        for i in range(_random.randint(min_l, max_l)))


def s2b(text: str) -> bytes | None:
    """將字串轉為bytes
    """

    try:
        if is_str(text): return bytes(text, 'utf-8')
        if not is_bytes(text): raise ValueError('Data is not string or bytes!')
        return text
    except:
        return None


def b2s(byte: bytes) -> str | None:
    """將bytes轉為字串
    """

    try:
        if is_bytes(byte): return bytes.decode(byte)
        if not is_str(byte): raise ValueError('Data is not bytes or string!')
        return byte
    except:
        return None


# Text

def search_text(pattern: _re.Pattern, text: str):
    """搜尋指定字串並回傳該字串
    """

    result = _re.search(pattern, text)
    return result.group(0) if result else None


# Time

def int_time(str_time: str, str_format: str = '%Y-%m-%d %a %H:%M:%S'):
    """將字串時間轉為timestamp
    """

    str_time = str_time.strftime(str_format)
    array_time = _time.strptime(str_time, str_format)
    return int(_time.mktime(array_time))

def now_time(get_timestamp: bool = False, str_format: str = '%Y-%m-%d %a %H:%M:%S'):
    """獲取現在時間
    """

    now = _datetime.datetime.now()
    return int(_time.mktime(now.timetuple())) \
        if get_timestamp else str(now.strftime(str_format))

def now_time_utc() -> int:
    """獲取UTC現在時間
    """

    return now_time(True) - 28800
