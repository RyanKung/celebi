import asyncpg
from pulsar.apps import Application
from pulsar import send, get_actor
from asyncio import ensure_future


class PostgresMonitor(Application):
    name = "postgres_arbiter"

    async def _connect(self, *args, **kwargs):
        self.conn = await asyncpg.connect(**self.cfg.pgconfigs)

    async def _execute(self, sql) -> str:
        return await self.conn.execute(sql)

    async def _fetchrow(self, sql) -> dict:
        return await self.conn.fetchrow(sql)

    async def _fetch(self, sql) -> dict:
        return await self.conn.fetch(sql)

    async def _transaction(self, sqls: list):
        async with self.conn.transaction():
            return [
                await self.conn.execute(sql)
                for sql in sqls
            ]

    async def worker_start(self, worker, exc=None):
        await self._connect()

    @classmethod
    async def query(cls, sql):
        arbiter = get_actor().get_actor(cls.cfg.name)
        actor = await arbiter.spawn()
        return await send(actor, 'run', cls._fetch, sql)

    @classmethod
    async def update(cls, sql):
        arbiter = get_actor().get_actor(cls.cfg.name)
        actor = await arbiter.spawn()
        return await send(actor, 'run', cls._fetch, sql)

    @classmethod
    async def insert(cls, sql):
        arbiter = get_actor().get_actor(cls.cfg.name)
        actor = await arbiter.spawn()
        return await send(actor, 'run', cls._fetchrow, sql)

    @classmethod
    async def execute(cls, sql: str) -> str:
        arbiter = get_actor().get_actor(cls.cfg.name)
        actor = await arbiter.spawn()
        return await send(actor, 'run', cls._execute, sql)

    @classmethod
    async def transaction(cls, sqls: list) -> str:
        arbiter = get_actor().get_actor(cls.cfg.name)
        actor = await arbiter.spawn()
        return await send(actor, 'run', cls._execute, sqls)
