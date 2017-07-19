from functools import partial
import asyncpg
from pulsar.apps import Application
from pulsar import send, get_application, get_actor
from functools import partial


async def test(self, exec=None):
    print('test')


class PostgresArbiter(Application):
    name = "postgres"

    def __init__(self, configs: dict, **kv) -> None:
        self.configs = configs
        super().__init__(**kv)

    async def connect(self, *args, **kwargs) -> asyncpg.Connection:
        conn = await asyncpg.connect(**self.configs)
        return conn

    async def disconnect(self, monitor, conn, *args, **kwargs) -> bool:
        try:
            await conn.close()
            return True
        except Exception as e:
            raise(e)
        finally:
            return False

    async def _execute(self, monitor, sql):
        res = await monitor.conn.execute(sql)
        return res

    async def monitor_start(self, monitor):
        print('start')
        conn = await self.connect()
        monitor.conn = conn
        # monitor.event('stopping').bind(
        #     partial(self.disconnect, conn=monitor.conn))

    def monitor_stop(self, monitor):
        #        self.disconnect()
        pass

    async def worker_start(self, worker, exc=None):
        print('bindent test')
        print('worker start')

    async def worker_stopping(self, worker, exc=None):
        print('worker stopping')

    @classmethod
    async def get_monitor(cls):
        actor = get_actor().get_actor('postgres')
        return actor

    @classmethod
    async def execute(cls, sql):
        arbiter = await cls.get_monitor()
        res = await send(arbiter, 'run', partial(cls._execute, cls), sql)
        return res
