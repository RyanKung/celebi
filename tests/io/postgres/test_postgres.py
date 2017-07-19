from tests.io.postgres import TestPostgresProcess
from celebi.io.postgres import PostgresArbiter
from celebi.schema.utils import split_file


class TestPostgres(TestPostgresProcess):

    async def test_callback(self):
        sqls = split_file('./celebi/schema/schema.sql')
        res = await PostgresArbiter.execute('DROP TABLE IF EXISTS datum;')
        res = await PostgresArbiter.execute(sqls[0])
        self.assertEqual('CREATE TABLE', res)
