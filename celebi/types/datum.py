#! -*- eval: (venv-workon "celebi"); -*-
import runpy
from types import ModuleType
from celebi.io.postgres import types
from celebi.io.postgres import QuerySet


__all__ = ['Datum']


class Datum(object):
    prototype = types.Table('qubit', [
        ('id', types.integer),
        ('name', types.varchar),
        ('entangle', types.varchar),
        ('is_stem', types.boolean),
        ('is_spout', types.boolean),
        ('monad', types.text),
        ('store', types.boolean),
        ('comment', types.text),
        ('flying', types.boolean),
        ('rate', types.integer)
    ])
    manager = QuerySet(prototype)

    @classmethod
    def create(cls, name, entangle=None,
               flying=True, is_stem=False, is_spout=False,
               store=False, *args, **kwargs) -> int:
        return cls.manager.insert(
            name=name,
            entangle=entangle,
            is_stem=is_stem,
            is_spout=is_spout,
            store=store,
            flying=flying, *args, **kwargs)

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
