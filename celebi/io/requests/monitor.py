from pulsar import get_application, get_actor, send
from pulsar.apps import Application
from pulsar.apps import http
from celebi.io.abstract import CelebiMonitor

__all__ = ['RequestMonitor']


class RequestMonitor(CelebiMonitor):
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
    async def request(cls, url, method='GET', *args, **kwargs):
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._request, url, method, *args, **kwargs)
