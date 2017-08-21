from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi
from celebi.core.decorators import jsonrpc
from celebi.types import Datum, Data
import json

__all__ = ['datum', 'Data']


@wsgi.router('/datum', methods=['GET', 'POST'])
@jsonrpc
async def datum(request: WsgiRequest) -> WsgiResponse:
    data = json.loads(await request.body_data())
    return await {
        'POST': Datum.create

    }[request.method](**data)


@wsgi.router('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jsonrpc
async def data(request: WsgiRequest) -> WsgiResponse:

    async def create():
        data = json.loads(await request.body_data())
        return await Data.create(**data)

    async def fetch():
        data = request.url_data
        return await Data.fetch(data['id'])
    return await {
        'POST': create,
        'GET': fetch

    }[request.method]()
