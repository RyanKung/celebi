import unittest

from pulsar import send
from pulsar.apps.test import dont_run_with_thread

from celebi.io.postgres import PostgresArbiter
from celebi.settings import POSTGRES_TEST


class TestPostgresThread(unittest.TestCase):
    app_cfg = None
    concurrency = 'thread'

    @classmethod
    def name(cls):
        return 'postgres'

    @classmethod
    async def setUpClass(cls):
        cls.arbiter = PostgresArbiter(configs=POSTGRES_TEST, workers=1)
        cls.app_cfg = await send('arbiter', 'run', cls.arbiter)
        print(cls.app_cfg)

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)


@dont_run_with_thread
class TestPostgresProcess(TestPostgresThread):
    concurrency = 'process'
