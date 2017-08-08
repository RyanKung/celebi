import time
from functools import wraps
from celebi.io.abstract import CelebiMonitor

__all__ = ['SchedulerMonitor']


class SchedulerMonitor(CelebiMonitor):
    name = 'scheduler_worker'
    tasks = []

    def task(self, fn, delta=1):
        self.tasks.append([delta, fn])

        @wraps(fn)
        def _(*args, **kwargs):
            return fn(*args, **kwargs)
        return _

    def monitor_task(self, monitor):
        [t() for t in self.tasks if int(time.time()) % t[0]]
