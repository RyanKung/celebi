import asyncpg
from pulsar.apps import Application


class PostgresArbiter(Application):
    name = "postgres"

    def __init__(self, configs: dict, **kv) -> None:
        self.configs = configs
        super().__init__(**kv)

    async def connect(self) -> asyncpg.Connection:
        conn = await asyncpg.connect(**self.configs)
        self.conn = conn
        return conn

    async def monitor_start(self, monitor):
        print('monitor starting')
        self.con = await self.connect()

    async def worker_start(self, worker, exc=None):
        print('worker start')

    async def worker_stopping(self, worker, exc=None):
        print('worker stopping')
