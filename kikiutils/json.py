import json as json

from typing import Union as Union


# Json operate

def read_json(path: str, encoding: str = 'utf-8'):
    """Read json file."""

    with open(path, 'r', encoding=encoding) as f:
        return json.loads(f.read())


def save_json(path: str, data: Union[dict, list], encoding: str = 'utf-8'):
    """Save json file."""

    with open(path, 'w', encoding=encoding) as f:
        return f.write(json.dumps(data))


# List

def add_item_to_list(_list: list, item):
    """Add item to list if item not in list."""

    if item not in _list:
        _list.append(item)


def remove_list_item(_list: list, item):
    """Remove list item."""

    if item in _list:
        _list.remove(item)
