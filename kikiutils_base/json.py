import json as _json

from typing import Union as _Union


# Json operate

def read_json(file_path: str, encoding: str = 'utf-8'):
    """Read json file."""

    with open(file_path, 'r', encoding=encoding) as f:
        return _json.loads(f.read())


def save_json(file_path: str, data: _Union[dict, list], encoding: str = 'utf-8'):
    """Save json file."""

    with open(file_path, 'w', encoding=encoding) as f:
        return f.write(_json.dumps(data))


# List

def add_item_to_list(_list: list, item, repeat: bool = False):
    """Add item to list."""

    if item not in _list:
        _list.append(item)


def remove_list_item(_list: list, item):
    """Remove list item."""

    if item in _list:
        _list.remove(item)
