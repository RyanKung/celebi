# -*- eval: (venv-workon "celebi"); -*-
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer
from celebi.core import wsgi


def server(**kwargs) -> WSGIServer:
    return WSGIServer(callable=WsgiHandler((wsgi, )), **kwargs)
