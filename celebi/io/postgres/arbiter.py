import asyncpg
from pulsar import as_coroutine
from pulsar.apps import Application


class PostgresArbiter(Application):
    name = "postgres"

    async def monitor_start(self, monitor):
        self.conn = await self.connect()
        print('monitor start')

    async def worker_start(self, worker, exc=None):
        if not exc and self.name not in worker.servers:
            server = await self.create_server(worker)
            server.bind_event('stop', lambda _, **kw: worker.stop())
            worker.servers[self.name] = server

    async def worker_stopping(self, worker, exc=None):
        server = worker.servers.get(self.name)
        if server:
            await server.close()
        close = getattr(self.cfg.callable, 'close', None)
        if hasattr(close, '__call__'):
            try:
                await as_coroutine(close())
            except Exception:
                pass

    def worker_info(self, worker, info):
        server = worker.servers.get(self.name)
        if server:
            info['%sserver' % self.name] = server.info()
        return info

    async def connect(self) -> asyncpg.Connection:
        conn = await asyncpg.connect(user='ryankung', password='pi3.1415926',
                                     database='database', host='127.0.0.1')
        self.conn = conn
        return conn
