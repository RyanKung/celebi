from typing import Iterable
import asyncpg
from asyncpg import Record
from pulsar.apps import Application
from pulsar import send, get_actor
from pulsar.utils.config import Config
from celebi.settings import POSTGRES


class PostgresArbiter(Application):
    name = "postgres"
    cfg = Config(apps=['asyncpg'], pgconf=POSTGRES)

    def __init__(self, configs: dict, **kv) -> None:
        self.configs = configs
        super().__init__(**kv)

    async def connect(self, *args, **kwargs):
        return await asyncpg.connect(**self.configs)

    @staticmethod
    async def _execute(actor, sql) -> str:
        return await actor.conn.execute(sql)

    @staticmethod
    async def _fetch(actor, sql) -> dict:
        res = await actor.conn.fetchrow(sql)
        return dict(res)

    @staticmethod
    async def _transaction(actor, sqls) -> str:
        async with actor.conn.transaction():
            return [await actor.conn.execute(s) for s in sqls]

    async def monitor_start(self, monitor, exec=None):
        monitor.conn = await asyncpg.connect(**self.cfg.pgconf)

    async def monitor_stopping(self, monitor, exec=None):
        monitor.conn.terminate()

    async def worker_start(self, worker, exc=None):
        if not worker.is_arbiter or worker.is_monitor:
            worker.conn = await asyncpg.connect(**self.cfg.pgconf)

    async def worker_stopping(self, worker, exc=None):
        if not worker.is_arbiter or worker.is_monitor:
            if hasattr(worker, 'conn'):
                worker.conn.terminate()

    def get_monitor(self):
        return get_actor().get_actor('postgres')

    async def execute(self, sql: str) -> str:
        arbiter = self.get_monitor()
        return await send(arbiter, 'run', self._execute, sql)

    async def fetch(self, sql: str) -> Record:
        arbiter = self.get_monitor()
        return await send(arbiter, 'run', self._fetch, sql)

    async def transaction(self, sqls: Iterable[str]) -> str:
        arbiter = self.get_monitor()
        return await send(arbiter, 'run', self._transaction, sqls)
