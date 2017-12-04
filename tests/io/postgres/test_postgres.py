from tests.io.postgres import TestPostgresProcess


class TestPostgres(TestPostgresProcess):

    async def test_CRUD(self):
        res = await self.monitor.execute('DROP TABLE IF EXISTS Test;')
        self.assertEqual('DROP TABLE', res)
        res = await self.monitor.execute('CREATE TABLE Test(id serial primary key, name varchar(200))')
        self.assertEqual('CREATE TABLE', res)

        res = await self.monitor.execute("INSERT Into Test(name) VALUES ('test')")
        self.assertEqual('INSERT 0 1', res)
        res = await self.monitor.fetch("select * from Test")
        self.assertEqual(res, [{'id': 1, 'name': 'test'}])

        res = await self.monitor.transaction(["INSERT Into Test(name) VALUES ('test')"] * 10)
        self.assertEqual(['INSERT 0 1'] * 10, res)
