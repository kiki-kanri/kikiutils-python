import json

from functools import wraps
from sanic import Request, text
from validator import validate as _validate

from .check import isdict
from .classes import DataTransmissionSecret


# DataTransmission

def data_transmission_api(
    *transmission_classes: DataTransmissionSecret,
    parse_json: bool = True
):
    def decorator(view_func):
        @wraps(view_func)
        async def wrapped_view(rq: Request, *args, **kwargs):
            # 檢查資料
            try:
                request_data: dict = rq.json
            except:
                request_data = {}

                for k in rq.form:
                    request_data[k] = rq.form.get(k)

            if len(request_data) != 1:
                return text('', 404)

            # 獲取加密後資料
            value = list(request_data.values())[0]

            # 解密資料並處理
            for transmission_class in transmission_classes:
                data: dict = transmission_class.process_hash_data(value)

                if data is not None:
                    break
            else:
                return text('', 404)

            if parse_json:
                for k, v in data.items():
                    try:
                        data[k] = json.loads(v)
                    except:
                        pass

            # 執行Function
            result = await view_func(
                rq,
                request_data=data,
                *args,
                **kwargs
            )

            # 處理Response
            response_data = {
                'success': True
            }

            if isdict(result):
                response_data.update(result)
            elif result is None:
                response_data['success'] = False
            elif result != True:
                return result

            return text(transmission_class.hash_data(response_data))

        return wrapped_view

    return decorator


# Validate

def validate(
    rules: dict,
    parse_json: bool = False,
    use_dict: bool = False
):
    """Validate request data."""

    def decorator(view_func):
        @wraps(view_func)
        async def wrapped_view(request: Request, *args, **kwargs):
            # 獲取資料並驗證
            request_data: dict[str, list[str]] = request.form

            for k, v in request_data.items():
                request_data[k] = v[0].strip()

                # Json轉換
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

                return await view_func(request, *args, **kwargs)

            return text('', 422)

        return wrapped_view

    return decorator
