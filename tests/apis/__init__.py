import unittest

from pulsar import send, get_application, get_actor
from pulsar.apps.http import HttpClient
from pulsar.apps.test import dont_run_with_thread

from celebi import wsgi, apis, WSGIServer, WsgiHandler


def server(**kwargs):
    return WSGIServer(callable=WsgiHandler((wsgi, )), **kwargs)


class TestCelebiThread(unittest.TestCase):
    app_cfg = None
    concurrency = 'thread'

    @classmethod
    def name(cls):
        return 'celebi_' + cls.concurrency

    @classmethod
    async def setUpClass(cls):
        s = server(name=cls.name(), concurrency=cls.concurrency,
                   bind='127.0.0.1:0')
        cls.app_cfg = await send('arbiter', 'run', s)
        cls.uri = 'http://{0}:{1}'.format(*cls.app_cfg.addresses[0])
        cls.client = HttpClient()

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)

    async def testMeta(self):
        app = await get_application(self.name())
        self.assertEqual(app.name, self.name())
        monitor = get_actor().get_actor(app.name)
        self.assertTrue(monitor.is_running())
        self.assertEqual(app, monitor.app)
        self.assertEqual(str(app), app.name)
        self.assertEqual(app.cfg.bind, '127.0.0.1:0')


@dont_run_with_thread
class TestCelebiProcess(TestCelebiThread):
    concurrency = 'process'
