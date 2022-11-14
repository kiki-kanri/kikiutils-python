from typing import Union as _Union

from .check import isint_or_digit as _isint_or_digit


# Number

def get_int_data(data: _Union[str, int], default = None):
    """Input int or string, if input value is not int or isdigit, return default value.
    """

    return int(data) if _isint_or_digit(data) else default
