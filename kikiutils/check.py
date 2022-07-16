import io as _io
import os as _os
import re as _re
import requests as _requests

from .file import get_file_mime


TYPE_BYTES = type(bytes())
TYPE_DICT = type(dict())
TYPE_INT = type(int())
TYPE_LIST = type(list())
TYPE_STR = type(str())


# Check

def check_domain(domain: str):
    """Check domain ping."""

    domain = _re.sub(r'[;|&\-\s​]', '', domain)
    return _os.system(f'ping -c 1 -s 8 {domain}') == 0


def check_email(email: str):
    """Check email format and ping the domain."""

    if _re.match(r'.*[+\-*/\\;&|\s​].*', email):
        return False
    return check_domain(email.split('@')[-1])


def check_file_type(
    file: bytes | _io.BytesIO | _io.FileIO,
    allow_types: set,
    file_mime: list = None
):
    """Check if the file type is in the allowed list."""

    if not file_mime:
        file_mime = get_file_mime(file)
    return file_mime[0] in allow_types


def check_file_ext(
    file: bytes | _io.BytesIO | _io.FileIO,
    allow_exts: set,
    file_mime: list = None
):
    """Check if the file ext is in the allowed list."""

    if not file_mime:
        file_mime = get_file_mime(file)
    return file_mime[1] in allow_exts


def isint_or_digit(text: int | str):
    """Check if the value is int or isdigit."""

    return isint(text) or (isstr(text) and text.isdigit())


def isbytes(*args):
    """Determine whether it is bytes."""

    return all([type(arg) == TYPE_BYTES for arg in args])


def isdict(*args):
    return all([type(arg) == TYPE_DICT for arg in args])


def isfile(*args):
    return all([_os.path.isfile(arg) for arg in args])


def isint(*args):
    """Determine whether it is int."""

    return all([type(arg) == TYPE_INT for arg in args])


def islist(*args):
    return all([type(arg) == TYPE_LIST for arg in args])


def isstr(*args):
    """Determine whether it is str."""

    return all([type(arg) == TYPE_STR for arg in args])


def response_is_ok(
    response: _requests.Response,
    only_html: bool = True
) -> bool:
    """Check whether the response responds normally."""

    return response and 200 <= response.status_code < 300 and (not only_html or 'text/html' in response.headers['Content-Type'])
