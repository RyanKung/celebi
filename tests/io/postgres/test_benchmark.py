from celebi.settings import POSTGRES_TEST
from tests.io.postgres import TestPostgresProcess
import asyncpg
import time


class TestBenchmark(TestPostgresProcess):

    async def setUpPG(self):
        res = await self.monitor.execute('DROP TABLE IF EXISTS Test;')
        self.assertEqual('DROP TABLE', res)
        res = await self.monitor.execute('CREATE TABLE Test(id serial primary key, name varchar(200))')
        self.assertEqual('CREATE TABLE', res)

    async def test_brenchmark(self):
        count = 1000
        bg_time = time.time()
        res = [await self.monitor.transaction([s] * 10) for s in ["INSERT Into Test(name) VALUES ('test')"] * count]
        self.assertEqual(len(res), count)
        end_time = time.time()
        print('Benchmark:: Call transaction(insert x 10) %s time cost %s With Actor model Asyncpg' %
              (count, end_time - bg_time))

    async def test_pure_asyncpg_brenchmark(self):

        count = 1000
        bg_time = time.time()
        res = []
        async with asyncpg.create_pool(min_size=20, max_size=20, **POSTGRES_TEST) as pool:
            for s in ["INSERT Into Test(name) VALUES ('test')"] * count:
                async with pool.acquire() as con:
                    async with con.transaction():
                        res += [await con.execute(s) for s in [s] * 10]
        end_time = time.time()
        print('Benchmark:: Call transaction(insert x 10) %s time cost %s with Origin Asyncpg' %
              (count, end_time - bg_time))
        self.assertEqual(1, 1)
