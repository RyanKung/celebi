#! -*- eval: (venv-workon "celebi"); -*-
import time
import json
from celebi.io.postgres import types
from celebi.io.postgres import QuerySet


__all__ = ['Data', 'Datum']


class Data(object):
    prototype = types.Table('ts_data', [
        ('id', types.integer),
        ('name', types.varchar),
        ('comment', types.text),
    ])
    manager = QuerySet(prototype)

    @classmethod
    async def create(cls, *args, **kwargs) -> str:
        return await cls.manager.insert(*args, **kwargs)

    @classmethod
    async def fetch(cls, did) -> str:
        return await cls.manager.get_by(id=did)

    @classmethod
    async def delete(cls, did) -> str:
        return await cls.manager.delete(did)

    @classmethod
    async def update(cls, did, data) -> str:
        return await cls.manager.update(did, **data)


class Datum(object):
    prototype = types.Table('ts_datum', [
        ('id', types.integer),
        ('ts', types.timestamp),
        ('dataset', types.integer),
        ('datum', types.json),
        ('tags', types.text)
    ])
    manager = QuerySet(prototype)

    @classmethod
    async def create(cls, dataset, datum, tags=[], ts=time.time()):
        return await cls.manager.insert(
            dataset=dataset,
            datum=json.dumps(datum),
            tags=','.join(tags),
            ts=ts
        )

    @classmethod
    async def fetch(cls, did) -> str:
        return await cls.manager.get_by(id=did)

    @classmethod
    async def delete(cls, did) -> str:
        return await cls.manager.delete(did)

    @classmethod
    async def update(cls, did, data) -> str:
        return await cls.manager.update(did, **data)
