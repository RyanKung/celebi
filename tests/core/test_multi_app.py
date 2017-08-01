import unittest
from pulsar import send, get_application
from celebi import ComposedApp


class TestComposedApp(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.arbiter = ComposedApp()
        cls.app_cfg = await send('arbiter', 'run', cls.arbiter)

    async def test_get_monitor(self):
        print(self.arbiter.apps())
        postgres = await get_application('celebi')
        wsgi = await get_application('postgres_celebi')
        self.assertTrue(postgres)
        self.assertTrue(wsgi)
