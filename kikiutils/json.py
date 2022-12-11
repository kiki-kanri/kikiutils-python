from aiofiles import open as async_open
from orjson import dumps as odumps, loads as oloads
from typing import Union as Union


# Json operate

async def async_read_json(path: str):
    """Async read json file with orjson."""

    async with async_open(path, 'rb') as f:
        return oloads(await f.read())


async def async_save_json(path: str, data: Union[dict, list]):
    """Async save json file with orjson."""

    async with async_open(path, 'wb') as f:
        return await f.write(odumps(data))


def read_json(path: str):
    """Read json file with orjson."""

    with open(path, 'rb') as f:
        return oloads(f.read())


def save_json(path: str, data: Union[dict, list]):
    """Save json file with orjson."""

    with open(path, 'wb') as f:
        return f.write(odumps(data))
