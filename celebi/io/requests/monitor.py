from pulsar import get_application, get_actor, send
from pulsar.apps import Application
from pulsar.apps import http

__all__ = ['RequestMonitor']


class RequestMonitor(Application):
    name = 'request_worker'

    async def monitor_start(self, monitor, exec=None):
        monitor.sessions = http.HttpClient()

    async def monitor_stopping(self, monitor, exec=None):
        if hasattr(monitor, 'sessions'):
            monitor.sessions

    async def _request(actor, url, method, **args):
        async with actor.sessions as sessions:
            res = await getattr(sessions, method.lower())(url, **args)
        return res

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

    @classmethod
    async def request(cls, url, method='GET', *args, **kwargs):
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._request, url, method, *args, **kwargs)
