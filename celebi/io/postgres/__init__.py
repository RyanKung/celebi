from celebi.settings import POSTGRES
from .postgres import Postgres
from .queryset import QuerySet

__all__ = [
    'QuerySet',
    'Postgres',
    'database'
]


database = Postgres(POSTGRES)
QuerySet.bind(database)
