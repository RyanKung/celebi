import asyncio
from typing import Any
from collections import defaultdict

__all__ = ['configdict']


def configdict(cases: dict, other: Any) -> defaultdict:
    assert other in cases.keys(), 'cases should include default cases'
    return defaultdict(lambda: other)(cases)


def retry(fn, times=3):
    async def _(*args, **kwargs):
        for t in range(0, times):
            asyncio.sleep(t * 5)
            try:
                res = await fn(*args, **kwargs)
            except:
                continue
            if res:
                return res
    return _
