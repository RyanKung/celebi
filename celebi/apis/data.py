from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi
from celebi.core.decorators import jsonrpc
from celebi.types import Datum, Data

__all__ = ['datum', 'Data']


@wsgi.router('/datum', methods=['GET', 'POST'])
@jsonrpc
async def datum(request: WsgiRequest) -> WsgiResponse:
    data = request.json()
    return await {
        'POST': Datum.create

    }[request.method](**data)


@wsgi.router('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jsonrpc
async def data(request: WsgiRequest) -> WsgiResponse:
    data = request.json()
    return await {
        'POST': Datum.create

    }[request.method](**data)
