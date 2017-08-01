from pulsar import Config
from pulsar.apps import MultiApp
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer
from celebi.core import wsgi
from celebi import apis
from celebi.io import PostgresMonitor
from celebi.settings import POSTGRES

__all__ = ['apis', 'wsgi', 'ComposedApp']


class ComposedApp(MultiApp):
    name = 'celebi'
    cfg = Config(pgconf=POSTGRES)

    def build(self):
        yield self.new_app(WSGIServer, callable=WsgiHandler((wsgi, )))
        yield self.new_app(PostgresMonitor, worker=10)
