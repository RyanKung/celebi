#! -*- eval: (venv-workon "celebi"); -*-
import runpy
import time
from types import ModuleType
from jirachi.io.postgres import types
from jirachi.io.postgres import QuerySet
from jirachi.io.scheduler import SchedulerMonitor as scheduler


__all__ = ['Data', 'Datum']


class Data(object):
    prototype = types.Table('ts_data', [
        ('id', types.integer),
        ('name', types.varchar),
        ('is_spout', types.boolean),
        ('generator', types.text),
        ('comment', types.text),
        ('flying', types.boolean),
        ('rate', types.integer)
    ])
    manager = QuerySet(prototype)

    @classmethod
    async def create(cls, name,
                     flying=True, is_spout=False, *args, **kwargs) -> str:
        return await cls.manager.insert(
            name=name,
            is_spout=is_spout,
            flying=flying, *args, **kwargs)

    @classmethod
    async def fetch(cls, did) -> str:
        return await cls.manager.get_by(id=did)

    @classmethod
    async def delete(cls, did) -> str:
        return await cls.manager.delete(did)

    @classmethod
    async def update(cls, did, data) -> str:
        return await cls.manager.update(did, **data)

    @scheduler.task
    @classmethod
    async def generate(cls):
        targets = cls.manager.get_by(is_spout=True)
        return [cls.exec_generator(t.generator) for t in targets]

    @staticmethod
    def require(name, *args, **kwargs) -> ModuleType:
        if '.py' not in name:
            name = name + '.py'
        module_dict = runpy.run_path(name)
        module = ModuleType(name)
        list(map(lambda x: setattr(module, *x), module_dict.items()))
        return module

    @staticmethod
    def __import__(name, *args, **kwargs) -> dict:
        whitelist = ['functools', 'operator',
                     'psutil',
                     'pandas', 'itertools']
        if name not in whitelist:
            return NotImplementedError
        return __import__(name, *args, **kwargs)

    @staticmethod
    def exec_generator(generator: str, glo={}, loc={}):
        builtins = dict(__builtins__,
                        require=Data.require,
                        __import__=Data.__import__)
        glo = glo or {
            '__builtins__': builtins
        }
        exec(generator, glo, loc)


class Datum(object):
    prototype = types.Table('ts_datum', [
        ('id', types.integer),
        ('ts', types.timestamp),
        ('index', types.text),
        ('dataset', types.integer),
        ('datum', types.json),
        ('tags', types.text)
    ])
    manager = QuerySet(prototype)

    @classmethod
    async def create(cls, dataset, index, datum, tags=[], ts=time.time()):
        return await cls.manager.insert(
            dataset=dataset,
            index=index,
            datum=datum,
            tags=','.join(tags),
            ts=ts)

    @classmethod
    async def fetch(cls, did) -> str:
        return await cls.manager.get_by(id=did)

    @classmethod
    async def delete(cls, did) -> str:
        return await cls.manager.delete(did)

    @classmethod
    async def update(cls, did, data) -> str:
        return await cls.manager.update(did, **data)
