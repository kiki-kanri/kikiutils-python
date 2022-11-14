from importlib import import_module as _import_module


def import_attribute(path: str):
    pkg, attr = path.rsplit('.', 1)
    return getattr(_import_module(pkg), attr)
