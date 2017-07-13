from typing import Callable, Hashable
import json
from functools import wraps
from asyncio import coroutine
from celebi.core.wsgi import success_response, error_response
from celebi.core.types import MaybeCorouteine


def maybe_async(op: bool=True) -> MaybeCorouteine:
    if op:
        return coroutine
    else:
        return lambda x: x


def jsonrpc(fn: Callable) -> Callable:
    @wraps(fn)
    @maybe_async()
    def _(request, *args, **kwargs) -> Hashable:
        try:
            result = yield from fn(request, *args, **kwargs)
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
