# -*- eval: (venv-workon "celebi"); -*-

ENV = 'DEV'

POSTGRES_TEST = {
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': 32770
}


POSTGRES_DEV = {
    'user': 'ryan',
    'password': 'pi3.1415926',
    'database': 'celebi',
    'host': '127.0.0.1'
}


POSTGRES = {
    'TEST': POSTGRES_TEST,
    'DEV': POSTGRES_DEV
}.get('ENV', POSTGRES_DEV)
