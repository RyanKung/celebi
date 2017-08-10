# -*- eval: (venv-workon "celebi"); -*-

import unittest
from pulsar import send, get_actor
from jirachi.io.remote import RemoteMonitorWSGI
from pulsar.apps.http import HttpClient


class TestRemoteMonitor(unittest.TestCase):

    @classmethod
    async def setUpClass(cls):
        cls.monitor = RemoteMonitorWSGI(workers=5)
        cls.app_cfg = await send('arbiter', 'run', cls.monitor)
        cls.client = HttpClient()
        cls.uri = 'http://{0}:{1}'.format(*cls.app_cfg.addresses[0])

    async def test_basic(self):
        url = self.uri + '/remote/remote_monitor/event/test/'
        resp = await self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        m = await self.monitor.get_monitor()
        self.assertEqual(m.name, 'remote_monitor')
        self.assertTrue(get_actor().get_actor(m.name))

    @classmethod
    def tearDownClass(cls):
        return send('arbiter', 'kill_actor', 'remote_monitor')
