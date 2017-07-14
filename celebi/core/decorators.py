from typing import Callable, Hashable
import json
from functools import wraps
from asyncio import coroutine
from celebi.core.wsgi import success_response, error_response
from celebi.core.types import MaybeCorouteine, Handler, Request
from asyncio import iscoroutine, iscoroutinefunction


__all__ = ['maybe_async', 'jsonrpc']


def maybe_async(fn: Callable) -> Callable[..., MaybeCorouteine]:
    if iscoroutinefunction(fn):
        return coroutine
    else:
        return lambda x: x


def jsonrpc(fn: Callable) -> Handler:
    @wraps(fn)
    @maybe_async(fn)
    def _(request: Request, *args, **kwargs) -> Hashable:
        try:
            result = fn(request, *args, **kwargs)
            if iscoroutine(result):
                result = yield from result
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
