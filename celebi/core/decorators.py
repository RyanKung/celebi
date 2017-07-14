from typing import Callable, Any
import json
from functools import wraps
from asyncio import coroutine
from celebi.core.wsgi import success_response, error_response
from celebi.core.types import (MaybeCorouteine, Handler,
                               Response, Maybe)
from asyncio import iscoroutinefunction


__all__ = ['maybe_async', 'jsonrpc']


def maybe_async(fn: Callable) -> Callable[..., MaybeCorouteine]:
    if iscoroutinefunction(fn):
        return coroutine
    else:
        return lambda x: x


def maybe_coro_cps(fn: Callable, context: Callable[[Maybe], Response]):
    @wraps(fn)
    @maybe_async(fn)
    def _(*args, **kwargs):
        try:
            if iscoroutinefunction(fn):
                result = yield from fn(*args, **kwargs)
            else:
                result = fn(*args, **kwargs)
        except Exception as e:
            result = e
        return context(result)
    return _


def jsonrpc(fn: Callable) -> Handler:
    def error(e: Exception) -> Response:
        res = dict(result=None, error=e.args, id=1)
        return error_response(json.dumps(res).encode())

    def just(r: dict) -> Response:
        res = dict(result=r, error=None, id=1)
        return success_response(json.dumps(res).encode())

    def handler(res: Maybe[Any, Exception]) -> Response:
        if isinstance(res, Exception):
            return error(res)
        else:
            return just(res)

    return maybe_coro_cps(fn, handler)
