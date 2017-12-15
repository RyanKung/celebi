import unittest
import time
from pulsar import send
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
        await Data.update(res['id'], {
            'comment': 'test comment 2'
        })
        data = await Data.fetch(res['id'])
        assert data['comment'] == 'test comment 2'
        await Data.delete(res['id'])
        data = await Data.fetch(res['id'])
        assert not bool(data)

    async def test_datum_crud(self):

        res = await Data.create(name='test', comment='test comment')
        did = res['id']

        datum = await Datum.create(
            dataset=did,
            datum={'hello': 'world'},
            ts=time.ctime(),
            tags=['a', 'b']
        )
        assert datum['id']
