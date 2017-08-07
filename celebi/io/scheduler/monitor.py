from pulsar import get_application, get_actor
from celebi.io.abstract import CelebiMonitor

__all__ = ['SchedulerMonitor']


class SchedulerMonitor(CelebiMonitor):
    name = 'scheduler_worker'

    @classmethod
    async def get_arbiter(cls):
        arbiter = get_actor().get_actor('arbiter')
        return arbiter

    @classmethod
    async def get_monitor(cls):
        async def get_monitor_via_arbiter():
            arbiter = get_actor().get_actor('arbiter')
            monitor_name = next(
                (m for m in arbiter.monitors if cls.name in m), None)
            monitor = await get_application(monitor_name)
            return monitor
        name = cls.cfg.name or cls.name
        monitor = get_actor().get_actor(name)
        return monitor or await get_monitor_via_arbiter()
