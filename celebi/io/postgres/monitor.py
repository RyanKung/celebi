from typing import Iterable
import asyncpg
from asyncpg import Record
from pulsar.apps import Application
from pulsar import send, get_actor, get_application

__all__ = ['PostgresMonitor']


class PostgresMonitor(Application):
    name = "postgres"

    async def connect(self, *args, **kwargs):
        return await asyncpg.connect(**self.cfg.pgconfigs)

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
        if hasattr(monitor, 'conn'):
            monitor.conn.terminate()

    async def worker_start(self, worker, exc=None):
        if not worker.is_arbiter or worker.is_monitor:
            worker.conn = await asyncpg.connect(**self.cfg.pgconf)

    async def worker_stopping(self, worker, exc=None):
        if not worker.is_arbiter or worker.is_monitor:
            if hasattr(worker, 'conn'):
                worker.conn.terminate()

    @classmethod
    async def execute(cls, sql: str) -> str:
        monitor = await cls.get_monitor()
        return await send(self, 'run', cls._execute, sql)

    @classmethod
    async def fetch(cls, sql: str) -> Record:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._fetch, sql)

    @classmethod
    async def transaction(cls, sqls: Iterable[str]) -> str:
        monitor = await cls.get_monitor()
        return await send(monitor, 'run', cls._transaction, sqls)

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
