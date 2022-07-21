import json as _json

from .check import isbytes as _isbytes, islist as _islist
from .string import b2s as _b2s, s2b as _s2b
from redis import Redis as _Redis
from typing import Union


class Redis:
    def __init__(self, *redis_args, **redis_kwargs) -> None:
        self.redis = _Redis(*redis_args, **redis_kwargs)

    def set(
        self,
        name: Union[int, str],
        value,
        *args,
        **kwargs
    ):
        if not _isbytes(value):
            if _islist(value) or type(value) == type(dict()):
                value = _json.dumps(value)

            value = _s2b(value)

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
            data = _b2s(data)

            try:
                json_data = _json.loads(data)
                data = json_data
            except:
                pass

        return data

    def delete(self, *names):
        return self.redis.delete(*names)

    def delete_all(self):
        keys = self.redis.keys()
        if len(keys):
            return self.redis.delete(*keys)
        return 0
