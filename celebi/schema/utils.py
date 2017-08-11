from pulsar import get_event_loop
from celebi.settings import POSTGRES
import asyncpg


def split_file(filename: str) -> list:
    with open(filename, 'r') as f:
        data = ''.join(map(lambda l: l.strip(), f.readlines()))
        return [q for q in data.split(';') if q]


def init_db():
    drop_sqls = split_file('celebi/schema/drop.sql')

    create_sqls = split_file('celebi/schema/schema.sql')
    loop = get_event_loop()

    async def process():
        conn = await asyncpg.connect(**POSTGRES)
        res = [await conn.execute(sql) for sql in drop_sqls + create_sqls]

        return res
    return loop.run_until_complete(process())
