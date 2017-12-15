# -*- eval: (venv-workon "celebi"); -*-
import os

ENV = os.getenv('ENV') or 'TEST'

POSTGRES_TEST = {
    'user': 'postgres',
    'password': '',
    'host': 'postgres',
    'port': 5432
}


POSTGRES_DEV = {
    'user': 'postgres',
    'password': '',
    'host': '127.0.0.1',
    'port': 32770
}

POSTGRES = {
    'TEST': POSTGRES_TEST,
    'DEV': POSTGRES_DEV
}.get(ENV, POSTGRES_TEST)

RABBITMQ_TEST = "amqp://guest:guest@rabbitmq:5672/%2F"
RABBITMQ_DEV = "amqp://guest:guest@localhost:32773/%2F"
RABBITMQ = {
    'TEST': RABBITMQ_TEST,
    'DEV': RABBITMQ_DEV
}.get(ENV, RABBITMQ_TEST)
