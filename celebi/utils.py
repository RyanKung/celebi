import asyncio
from typing import Any
from collections import defaultdict
import traceback

__all__ = ['configdict']


def configdict(cases: dict, other: Any) -> defaultdict:
    assert other in cases.keys(), 'cases should include default cases'
    return defaultdict(lambda: other)(cases)


def retry(fn, times=3):
    async def _(*args, **kwargs):
        for t in range(0, times):
            await asyncio.sleep(t * 5)
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                if t + 1 != times:
                    traceback.print_exc()
                    continue
                raise(e)
            print('Retry %snd time, Waiting %s seconds' % (t + 1, (t + 1) * 5))
    return _


def ensure(fn):
    def _(*args, **kwargs):
        return asyncio.ensure_future(fn(*args, **kwargs))
    return _
