import unittest
from pulsar import send, get_application
from celebi.settings import POSTGRES
from celebi.io.postgres import PostgresMonitor
from celebi.types.datatype import Data, Datum


class TestDaum(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.monitor = PostgresMonitor(workers=10, pgconfigs=POSTGRES)
        await send('arbiter', 'run', cls.monitor)

    async def test_data_crud(self):
        res = await Data.create(name='test', comment='test comment')
        data = await Data.fetch(res['id'])
        assert data['comment'] == 'test comment'
        await Data.delete(res['id'])
        data = await Data.fetch(res['id'])
        assert not bool(data)

    def test_datum_crud(self):
        pass
