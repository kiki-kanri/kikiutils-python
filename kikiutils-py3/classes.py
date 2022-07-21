import json as _json

from redis import Redis as _Redis
from typing import Union

from .check import isbytes as _isbytes, islist as _islist
from .string import b2s as _b2s, s2b as _s2b


class Redis:
    def __init__(self, *redis_args, **redis_kwargs) -> None:
        self.redis = _Redis(*redis_args, **redis_kwargs)

    def bytes2data(self, data):
        if _isbytes(data):
            data = _b2s(data)

            try:
                json_data = _json.loads(data)
                data = json_data
            except:
                pass

        return data

    def data2bytes(self, data):
        if not _isbytes(data):
            if _islist(data) or type(data) == type(dict()):
                data = _json.dumps(data)

            data = _s2b(data)

        return data

    def set(
        self,
        name: Union[int, str],
        value,
        *args,
        **kwargs
    ):
        value = self.data2bytes(value)

        return self.redis.set(
            name,
            value,
            *args,
            **kwargs
        )

    def get(self, name, *args, **kwargs):
        data = self.redis.get(
            name,
            *args,
            **kwargs
        )

        if data != None:
            data = self.bytes2data(data)

        return data

    def delete(self, *names):
        return self.redis.delete(*names)

    def delete_all(self):
        keys = self.redis.keys()
        if len(keys):
            return self.redis.delete(*keys)
        return 0
