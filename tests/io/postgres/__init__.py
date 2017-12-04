import unittest

from pulsar import send
from pulsar.apps.test import dont_run_with_thread
from pulsar import Config

from jirachi.io.postgres import PostgresMonitor
from celebi.settings import POSTGRES_TEST


class TestPostgresThread(unittest.TestCase):
    app_cfg = None
    concurrency = 'thread'

    @classmethod
    def name(cls):
        return 'postgres_celebi'

    @classmethod
    async def setUpClass(cls):
        cfg = Config(pgconf=POSTGRES_TEST, name='postgres_celebi')
        cls.monitor = PostgresMonitor(
            cfg=cfg, workers=50)
        cls.app_cfg = await send('arbiter', 'run', cls.monitor)

    @classmethod
    async def tearDownClass(cls):
        if cls.app_cfg is not None:
            return await send('arbiter', 'kill_actor', cls.app_cfg.name)


@dont_run_with_thread
class TestPostgresProcess(TestPostgresThread):
    concurrency = 'process'
