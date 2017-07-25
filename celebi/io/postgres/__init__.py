from .arbiter import PostgresArbiter

__all__ = ['PostgresArbiter']


def postgres_arbiter(**kwargs) -> PostgresArbiter:
    return PostgresArbiter(**kwargs)
