import io
import os
import shutil

from typing import Callable, Union


# File

def create_dir(path: str):
    """Create dir."""

    try:
        os.makedirs(path)
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
        shutil.rmtree(path)
        return True
    except:
        return False


def save_file(
    path: str,
    file: Union[bytes, io.BytesIO, io.FileIO, str],
    replace: bool = True
):
    """Save file."""

    mode = 'w' if isinstance(file, str) else 'wb'

    try:
        if os.path.exists(path) and not replace:
            raise FileExistsError()
        if getattr(file, 'read', None):
            file = file.read()
        with open(path, mode) as f:
            f.write(file)
        return True
    except:
        return False


def save_file_as_bytesio(
    save_fnc: Callable,
    get_bytes: bool = False,
    **kwargs
):
    """Save file to io.BytesIO."""

    with io.BytesIO() as output:
        save_fnc(output, **kwargs)
        file_bytes = output.getvalue()

    if get_bytes:
        return file_bytes
    return io.BytesIO(file_bytes)


def move_file(path: str, target_path: str):
    """Move file or dir."""

    try:
        shutil.move(path, target_path)
        return True
    except:
        return False


def rename(path: str, name: str):
    """Rename file or dir."""

    try:
        os.rename(path, name)
        return True
    except:
        return False


def del_file(path: str):
    """Del file."""

    try:
        os.remove(path)
        return True
    except:
        return False
