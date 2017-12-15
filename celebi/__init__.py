# -*- eval: (venv-workon "celebi"); -*-

from pulsar.apps import MultiApp
from functools import partial
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer
from celebi.settings import POSTGRES, RABBITMQ
from celebi.core import wsgi
from celebi.io.postgres import PostgresMonitor
from celebi import apis
from celebi.io.qubit import (
    Measurement,
    Entanglement,
    QubitMonitor
)

__all__ = ['apis', 'wsgi', 'ComposedApp', 'ComposedIO']


class ComposedIO(MultiApp):
    name = 'arbiters'

    def build(self):
        yield self.new_app(
            App=QubitMonitor,
            name='pikachu_monitor',
            exchange_type='fanout',
            exchange='test',
            processor=dict,
            measurements=[Measurement(
                name='test',
                spout=partial(dict, hello='world'),
                rate=1
            )],
            entanglements=[
                Entanglement(
                    name='test',
                    exchange='test',
                    rate=1,
                    amqp_url=RABBITMQ
                )
            ],
            amqp_cfg=RABBITMQ,
            workers=10
        )
        yield self.new_app(
            App=PostgresMonitor,
            workers=10,
            pgconfigs=POSTGRES
        )


class ComposedApp(MultiApp):
    name = 'celebi'

    def build(self):
        yield self.new_app(WSGIServer, callable=WsgiHandler((wsgi, )), bind="127.0.0.1:8964")
        yield self.new_app(ComposedIO)
