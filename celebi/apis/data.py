from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi
from celebi.core.decorators import jsonrpc

__all__ = ['datum']


@wsgi.router('/datum', methods=['GET', 'POST'])
@jsonrpc
async def datum(request: WsgiRequest) -> WsgiResponse:
    return {}


@wsgi.router('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jsonrpc
async def data(request: WsgiRequest) -> WsgiResponse:
    return {}
