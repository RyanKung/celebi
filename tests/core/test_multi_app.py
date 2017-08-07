import unittest
from pulsar import send, get_application, get_actor
from celebi.io.postgres import PostgresMonitor
from celebi import ComposedApp


class TestComposedApp(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.monitor = ComposedApp()
        cls.app_cfg = await send('arbiter', 'run', cls.monitor)

    async def test_get_monitor(self):
        wsgi = await get_application('celebi')
        postgres = await get_application('postgres_celebi')
        arbiter = get_actor().get_actor('arbiter')
        postgres1 = await PostgresMonitor.get_monitor()
        self.assertTrue(postgres)
        self.assertTrue(wsgi)
        self.assertTrue(arbiter)
        self.assertEqual(postgres1, postgres)
        self.assertTrue(hasattr(postgres, 'execute'))

    @classmethod
    def tearDownClass(cls):
        for app in cls.monitor.apps():
            send('arbiter', 'kill_actor', app.name)
