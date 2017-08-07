import unittest

from pulsar import send, get_actor
from pulsar.apps.test import dont_run_with_thread
from pulsar import Config

from celebi.io.postgres import PostgresMonitor
from pulsar.utils.exceptions import ImproperlyConfigured
from celebi.settings import POSTGRES_TEST


class TestPostgresThread(unittest.TestCase):
    app_cfg = None
    concurrency = 'thread'

    @classmethod
    def name(cls):
        return 'postgres'

    @classmethod
    async def setUpClass(cls):
        cfg = Config(pgconf=POSTGRES_TEST, name='postgres')
        cls.monitor = PostgresMonitor(
            cfg=cfg, workers=1, name='postgres_celebi')
        try:
            cls.app_cfg = await send('arbiter', 'run', cls.monitor)
        except ImproperlyConfigured:
            cls.app_cfg = get_actor().get_actor('postgres_celebi')

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)


@dont_run_with_thread
class TestPostgresProcess(TestPostgresThread):
    concurrency = 'process'
