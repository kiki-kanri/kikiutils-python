import random as _random
import re as _re
import string as _string

from typing import Union as _Union

from .check import isbytes as _isbytes, isstr as _isstr


_RANDOM_LETTERS = _string.ascii_letters + _string.digits


def random_str(min_l: int = 8, max_l: int = 8):
    return ''.join(_random.choice(_RANDOM_LETTERS) for i in range(_random.randint(min_l, max_l)))


def s2b(text: str) -> _Union[bytes, None]:
    """Convert string to bytes."""

    try:
        if _isstr(text):
            return bytes(text, 'utf-8')
        if not _isbytes(text):
            raise ValueError('Data is not string or bytes!')
        return text
    except:
        return None


def b2s(byte: bytes) -> _Union[str, None]:
    """Convert bytes to string."""

    try:
        if _isbytes(byte):
            return bytes.decode(byte)
        if not _isstr(byte):
            raise ValueError('Data is not bytes or string!')
        return byte
    except:
        return None


# Text

def search_text(
    pattern: _re.Pattern,
    text: str,
    group_index: int = 0,
    **kwargs
):
    """Search text by passern and return result."""

    result = _re.search(pattern, text, **kwargs)
    return result[group_index] if result else None
