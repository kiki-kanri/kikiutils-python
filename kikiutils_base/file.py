import io as _io
import magic as _magic
import os as _os
import shutil as _shutil

from pyclbr import Function as _Function
from typing import Union as _Union


# File

def create_dir(path: str):
    """Create dir."""

    try:
        _os.makedirs(path)
        return True
    except:
        return False


def clear_dir(path: str):
    """Clear dir. (Remove and create.)"""

    remove_dir(path)
    create_dir(path)


def read_file(path: str):
    """Read file."""

    try:
        with open(path, 'rb') as f:
            data = f.read()
            return data
    except:
        pass


def remove_dir(path: str):
    """Remove dir."""

    try:
        _shutil.rmtree(path)
        return True
    except:
        return False


def save_file(
    file: _Union[bytes, _io.BytesIO, _io.FileIO, str],
    path: str,
    replace: bool = True
):
    """Save file."""

    if type(file) == type(str()):
        file = bytes(file, 'utf-8')

    try:
        if _os.path.exists(path) and not replace:
            raise FileExistsError()
        if getattr(file, 'read', None):
            file = file.read()
        with open(path, 'wb') as f:
            f.write(file)
        return True
    except:
        return False


def save_file_as_bytesio(
    save_fnc: _Function,
    get_bytes: bool = False,
    **kwargs
):
    """Save file to io.BytesIO."""

    with _io.BytesIO() as output:
        save_fnc(output, **kwargs)
        file_bytes = output.getvalue()

    if get_bytes:
        return file_bytes
    return _io.BytesIO(file_bytes)


def move_file(path: str, target_path: str):
    """Move file or dir."""

    try:
        _shutil.move(path, target_path)
        return True
    except:
        return False


def rename(path: str, name: str):
    """Rename file or dir."""

    try:
        _os.rename(path, name)
        return True
    except:
        return False


def del_file(path: str):
    """Del file."""

    try:
        _os.remove(path)
        return True
    except:
        return False
