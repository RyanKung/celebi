from functools import partial
from typing import Callable
from pwsgi.router import BluePrint
from pulsar.apps.wsgi import WsgiResponse
from pulsar.apps.wsgi.handlers import WsgiHandler
from pulsar.apps.wsgi import WSGIServer


__all__ = ['wsgi', 'error_response', 'success_response']


wsgi: BluePrint = BluePrint('/')
success_response: Callable = partial(WsgiResponse, 200)
error_response: Callable = partial(WsgiResponse, 500)

response = success_response


def wsgi_server(**kwargs) -> WSGIServer:
    return WSGIServer(callable=WsgiHandler((wsgi, )), **kwargs)
