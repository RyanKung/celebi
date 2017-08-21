from pulsar import get_event_loop
from celebi.settings import POSTGRES_TEST
import asyncpg


def split_file(filename: str) -> list:
    with open(filename, 'r') as f:
        data = ''.join(map(lambda l: l.strip(), f.readlines()))
        return [q for q in data.split(';') if q]


async def async_init_db(config=POSTGRES_TEST):
    drop_sqls = split_file('celebi/schema/drop.sql')

    create_sqls = split_file('celebi/schema/schema.sql')
    conn = await asyncpg.connect(**config)
    res = [await conn.execute(sql) for sql in drop_sqls + create_sqls]

    return res


def init_db(config=POSTGRES_TEST):
    loop = get_event_loop()
    return loop.run_until_complete(async_init_db(config))
