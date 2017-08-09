import unittest
from pulsar import send
from celebi.io.remote import RemoteMonitorWSGI
from pulsar.apps.http import HttpClient


class TestRemoteMonitor(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.monitor = RemoteMonitorWSGI(workers=2)
        cls.app_cfg = await send('arbiter', 'run', cls.monitor)
        cls.client = HttpClient()
        cls.uri = 'http://{0}:{1}'.format(*cls.app_cfg.addresses[0])

    async def test_basic(self):
        url = self.uri
        resp = await self.client.post(url)
        self.assertTrue(resp.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        return send('arbiter', 'kill_actor', 'remote_monitor')
