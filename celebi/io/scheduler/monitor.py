# -*- eval: (venv-workon "celebi"); -*-

import time
from functools import wraps
from celebi.io.abstract import CelebiMonitor

__all__ = ['SchedulerMonitor']


class SchedulerMonitor(CelebiMonitor):
    name = 'scheduler_worker'
    _tasks = []

    def task(self, fn, rule=lambda t: int(t) % 1 == 0):
        self._tasks.append([rule, fn])

        @wraps(fn)
        def _(*args, **kwargs):
            return fn(*args, **kwargs)
        return _

    def monitor_task(self, monitor):
        [t[1]() for t in self._tasks if t[0](time.time())]
