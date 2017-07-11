from typing import Callable, Hashable
import json
from celebi.core.wsgi import success_response, error_response


def jsonrpc(fn: Callable) -> Callable:
    def _(request, *args, **kwargs) -> Hashable:
        try:
            res = dict(
                result=fn(*args, **kwargs),
                error=None,
                id=request.id
            )
            return success_response(json.dumps(res))
        except Exception as e:
            res = dict(
                result=None,
                error=e.regs,
                id=request.id
            )
            return error_response(dict(
                result=None,
                error=str(e),
                id=request.id
            ))
