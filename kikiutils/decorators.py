import json

from functools import wraps
from quart import request
from validator import validate as _validate

from .check import isdict
from .classes import DataTransmissionSecret


def data_transmission_api(
    *secret_classes: DataTransmissionSecret,
    parse_json: bool = True
):
    def decorator(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            request_values = await request.values

            if len(request_values) != 1:
                return '', 404

            value = list(request_values.values())[0]

            for secret_class in secret_classes:
                data: dict = secret_class.process_hash_data(value)

                if data is not None:
                    break
            else:
                return '', 404

            if parse_json:
                for k, v in data.items():
                    try:
                        data[k] = json.loads(v)
                    except:
                        pass

            result = await view_func(
                request_data=data,
                *args,
                **kwargs
            )

            response_data = {
                'success': True
            }

            if isdict(result):
                response_data.update(result)
            elif result is None:
                response_data['success'] = False
            elif result != True:
                return result

            return secret_class.hash_data(response_data)

        return wrapped_view

    return decorator


def validate(
    rules: dict,
    parse_json: bool = False,
    use_dict: bool = False
):
    """Validate request data."""

    def decorator(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            request_data: dict[str, str] = (await request.values).to_dict()

            for k, v in request_data.copy().items():
                request_data[k] = v.strip()

                if parse_json:
                    try:
                        request_data[k] = json.loads(request_data[k])
                    except:
                        pass

            result, data, _ = _validate(request_data, rules, True)

            if result:
                if use_dict:
                    kwargs['data'] = data
                else:
                    kwargs.update(data)

                return await view_func(*args, **kwargs)

            return '', 422

        return wrapped_view

    return decorator
