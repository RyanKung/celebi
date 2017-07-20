from functools import partial
import asyncpg
from asyncpg import Connection
from pulsar.apps import Application
from pulsar import send, get_actor


async def test(self, exec=None):
    print('test')


class PostgresArbiter(Application):
    name = "postgres"

    def __init__(self, configs: dict, **kv) -> None:
        self.configs = configs
        super().__init__(**kv)

    async def init(self, *args, **kwargs):
        return await asyncpg.create_pool(**self.configs)

    def terminate(self, monitor, *args, **kwargs):
        try:
            monitor.pool.terminate()
            return True
        except Exception as e:
            raise(e)
        finally:
            return False

    async def _execute(self, monitor, sql):
        async with monitor.pool.acquire() as conn:
            return await conn.execute(sql)

    async def monitor_start(self, monitor):
        print('monitor start')
        pool = await self.init()
        monitor.pool = pool
        monitor.event('stopping').bind(self.terminate)

    async def worker_start(self, worker, exc=None):
        print('bindent test')
        print('worker start')

    async def worker_stopping(self, worker, exc=None):
        print('worker stopping')

    @classmethod
    async def get_monitor(cls):
        return get_actor().get_actor('postgres')

    @classmethod
    async def execute(cls, sql):
        arbiter = await cls.get_monitor()
        return await send(arbiter, 'run', partial(cls._execute, cls), sql)
