import asyncpg
from pulsar.apps import Application
from pulsar import send, get_actor, get_application

__all__ = ['PostgresMonitor']


class PostgresMonitor(Application):
    name = "postgres_arbiter"

    async def _connect(self):
        return await asyncpg.connect(**self.cfg.pgconfigs)

    @staticmethod
    async def _execute(actor, sql) -> str:
        return str(
            await actor.conn.execute(sql)
        )

    @staticmethod
    async def _fetchrow(actor, sql) -> dict:
        return dict(
            await actor.conn.fetchrow(sql)
        )

    @staticmethod
    async def _fetch(actor, sql) -> dict:
        return list(
            map(dict, await actor.conn.fetch(sql))
        )

    @staticmethod
    async def _transaction(actor, sqls: list):
        async with actor.conn.transaction():
            return [
                await actor.conn.execute(sql)
                for sql in sqls
            ]

    async def monitor_start(self, monitor, exc=None):
        monitor.conn = await self._connect()

    async def worker_start(self, worker, exc=None):
        worker.conn = await self._connect()

    @classmethod
    async def query(cls, sql):
        arbiter = get_actor().get_actor(cls.name)
        app = await get_application(cls.name)
        actor = await arbiter.spawn(
            start=app.worker_start
        )
        return await send(actor, 'run', app._fetch, sql)

    @classmethod
    async def update(cls, sql):
        arbiter = get_actor().get_actor(cls.name)
        app = await get_application(cls.name)
        actor = await arbiter.spawn(
            start=app.worker_start
        )
        return await send(actor, 'run', app._fetch, sql)

    @classmethod
    async def insert(cls, sql):
        arbiter = get_actor().get_actor(cls.name)
        app = await get_application(cls.name)
        actor = await arbiter.spawn(
            start=app.worker_start
        )
        return await send(actor, 'run', app._fetchrow, sql)

    @classmethod
    async def execute(cls, sql: str) -> str:

        arbiter = get_actor().get_actor(cls.name)
        app = await get_application(cls.name)
        actor = await arbiter.spawn(
            start=app.worker_start
        )
        return await send(actor, 'run', app._execute, sql)

    @classmethod
    async def transaction(cls, sqls: list) -> str:
        arbiter = get_actor().get_actor(cls.name)
        app = await get_application(cls.name)
        actor = await arbiter.spawn(
            start=app.worker_start
        )
        return await send(actor, 'run', app._execute, sqls)
