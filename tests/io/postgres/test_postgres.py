from celebi.settings import POSTGRES_TEST
from tests.io.postgres import TestPostgresProcess
import asyncpg
import time


class TestPostgres(TestPostgresProcess):

    async def setUpPG(self):
        res = await self.arbiter.execute('DROP TABLE IF EXISTS Test;')
        self.assertEqual('DROP TABLE', res)
        res = await self.arbiter.execute('CREATE TABLE Test(id serial primary key, name varchar(200))')
        self.assertEqual('CREATE TABLE', res)

    async def test_CRUD(self):
        res = await self.arbiter.execute("INSERT Into Test(name) VALUES ('test')")
        self.assertEqual('INSERT 0 1', res)
        res = await self.arbiter.fetch("select * from Test")
        self.assertEqual(res, {'id': 1, 'name': 'test'})

        res = await self.arbiter.transaction(["INSERT Into Test(name) VALUES ('test')"] * 10)
        self.assertEqual(['INSERT 0 1'] * 10, res)

    # async def test_brenchmark(self):
    #     '''
    #     Benchmark:: Call transaction(insert x 10) 1000 time cost 8.52885127067566 With Actor modeling Asyncpg
    #     '''
    #     count = 1000
    #     bg_time = time.time()
    #     res = [await self.arbiter.transaction([s] * 10) for s in ["INSERT Into Test(name) VALUES ('test')"] * count]
    #     self.assertEqual(len(res), count)
    #     end_time = time.time()
    #     print('Benchmark:: Call transaction(insert x 10) %s time cost %s With Actor modeling Asyncpg' %
    #           (count, end_time - bg_time))

    # async def test_pure_asyncpg_brenchmark(self):
    #     '''
    #     Benchmark:: Call transaction(insert x 10) 1000 time cost 111.19546413421631 with Origin Asyncpg
    #     '''

    #     count = 1000
    #     bg_time = time.time()
    #     res = []
    #     for s in ["INSERT Into Test(name) VALUES ('test')"] * count:
    #         async with asyncpg.create_pool(**POSTGRES_TEST) as pool:
    #             async with pool.acquire() as con:
    #                 async with con.transaction():
    #                     res += [await con.execute(s) for s in [s] * 10]
    #     end_time = time.time()
    #     print('Benchmark:: Call transaction(insert x 10) %s time cost %s with Origin Asyncpg' %
    #           (count, end_time - bg_time))
    #     self.assertEqual(1, 1)
