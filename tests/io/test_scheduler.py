import unittest
from pulsar import send
from celebi.io.scheduler import SchedulerMonitor


class TestScheduler(unittest.TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.monitor = SchedulerMonitor(workers=1, name='scheduler_worker')
        await send('arbiter', 'run', cls.monitor)

    @classmethod
    def tearDownClass(cls):
        return send('arbiter', 'kill_actor', 'scheduler_worker')

    def testMeta(self):
        self.assertEqual(1, 1)
