# -*- eval: (venv-workon "celebi"); -*-

from pulsar.apps import MultiApp
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer
from celebi.core import wsgi
from celebi import apis
from celebi.types.abstract import (
    Measurement,
    Entanglement,
    Monitor
)

__all__ = ['apis', 'wsgi', 'ComposedApp', 'ComposedIO']


class ComposedIO(MultiApp):
    name = 'arbiters'

    def build(self):
        yield self.new_app(
            App=Monitor,
            name='pikachu_monitor',
            exchange_type='fanout',
            exchange='test',
            measurements=[Measurement()],
            entanglements=[Entanglement('test')],
            worker=10
        )


class ComposedApp(MultiApp):
    name = 'celebi'

    def build(self):
        yield self.new_app(WSGIServer, callable=WsgiHandler((wsgi, )), bind="127.0.0.1:8964")
        yield self.new_app(ComposedIO, worker=10)
