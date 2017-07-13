from typing import Callable, Hashable
import json
from functools import wraps
from celebi.core.wsgi import success_response, error_response


def jsonrpc(fn: Callable) -> Callable:
    @wraps(fn)
    async def _(request, *args, **kwargs) -> Hashable:
        try:
            result = await fn(request, *args, **kwargs),
            res = dict(
                result=result,
                error=None,
                id=1
            )
            return success_response(json.dumps(res).encode())
        except Exception as e:
            res = dict(
                result=None,
                error=e.args,
                id=1
            )
            return error_response(json.dumps(res).encode())
    return _
