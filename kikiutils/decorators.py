from functools import wraps
from inspect import iscoroutinefunction


def try_and_get_bool(view_func):
    """Run the function use try/catch.

    Returns False if there was an error. Otherwise return True.

    Supports async and sync function.
    """

    # Return async wrapped_view if view_func is coro
    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            try:
                await view_func(*args, **kwargs)
                return True
            except:
                return False
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            view_func(*args, **kwargs)
            return True
        except:
            return False
    return wrapped_view


def try_and_get_data(view_func):
    """Run the function use try/catch.

    Returns None if there was an error. Otherwise return the function result.

    Supports async and sync function.
    """

    # Return async wrapped_view if view_func is coro
    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            try:
                return await view_func(*args, **kwargs)
            except:
                pass
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except:
            pass
    return wrapped_view
