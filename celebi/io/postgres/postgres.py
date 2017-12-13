import asyncpg


class Postgres:
    async def __init__(self, config: dict):
        self.conn = await asyncpg.connect(**config)

    async def query(self, sql):
        return await self.conn.fetch(sql)

    async def update(self, sql):
        return await self.conn.fetch(sql)

    async def insert(self, sql):
        return await self.conn.fetchrow(sql)
