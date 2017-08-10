# -*- eval: (venv-workon "celebi"); -*-

from pulsar import Config
from pulsar.apps import MultiApp
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer
from celebi.core import wsgi
from celebi import apis
from jirachi.io.postgres import PostgresMonitor
from jirachi.io import RequestMonitor
from jirachi.io import SchedulerMonitor
from celebi.settings import POSTGRES

__all__ = ['apis', 'wsgi', 'ComposedApp', 'ComposedIO']


class ComposedIO(MultiApp):
    name = 'io'
    cfg = Config(pgconf=POSTGRES)

    def build(self):
        yield self.new_app(RequestMonitor, worker=10)
        yield self.new_app(PostgresMonitor, worker=10)
        yield self.new_app(SchedulerMonitor, worker=10)


class ComposedApp(MultiApp):
    name = 'celebi'

    def build(self):
        yield self.new_app(WSGIServer, callable=WsgiHandler((wsgi, )), bind="127.0.0.1:8964")
        yield self.new_app(ComposedIO, worker=10)
