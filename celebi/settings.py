# -*- eval: (venv-workon "celebi"); -*-

ENV = 'TEST'

POSTGRES_TEST = {
    'user': 'postgres',
    'password': '',
    'host': '127.0.0.1',
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
}.get('ENV', POSTGRES_TEST)
