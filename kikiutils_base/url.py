import urllib3 as _urllib3

_urllib3.disable_warnings()


# Url process

def get_host(url: str, get_raw_data: bool = False):
    """Get the host of the input url."""

    host = _urllib3.get_host(url)
    return host if get_raw_data else host[1]
