# -*- eval: (venv-workon "celebi"); -*-

from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi, response
from celebi.core.decorators import jsonrpc

__all__ = ['datum']


@wsgi.router('/datum', methods=['GET', 'POST'])
async def datum(request: WsgiRequest) -> WsgiResponse:
    return response('{}')


@wsgi.router('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jsonrpc
async def data(request: WsgiRequest) -> WsgiResponse:
    return {}
