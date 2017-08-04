from tests.io.postgres import TestPostgresProcess
from celebi.io.postgres import QuerySet
from celebi.io.postgres import types


class TestPostgresQueryset(TestPostgresProcess):

    async def setUpPG(self):
        res = await self.arbiter.execute('DROP TABLE IF EXISTS Test;')
        self.assertEqual('DROP TABLE', res)
        res = await self.arbiter.execute('CREATE TABLE Test(id serial primary key, name varchar(200))')
        self.assertEqual('CREATE TABLE', res)

    async def test_queryset(self):
        prototype = types.Table('Test', [
            ('name', types.varchar)
        ])
        manager = QuerySet(prototype)
        self.assertTrue(manager)
        ins = await manager.insert(name='abd')
        self.assertTrue(ins)
