import asyncpg
from asyncio import ensure_future


class Postgres:
    def __init__(self, config: dict):
        self.conn = ensure_future(asyncpg.connect(**config))

    async def query(self, sql):
        return await self.conn.fetch(sql)

    async def update(self, sql):
        return await self.conn.fetch(sql)

    async def insert(self, sql):
        return await self.conn.fetchrow(sql)
