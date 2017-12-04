from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi
from celebi.core.decorators import jsonrpc
from celebi.types import Datum, Data
import json

__all__ = ['datum', 'Data']


@wsgi.router('/datum', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@jsonrpc
async def datum(request: WsgiRequest) -> WsgiResponse:

    async def create():
        data = json.loads(await request.body_data())
        return await Datum.create(**data)

    async def fetch():
        data = request.url_data
        return await Datum.fetch(data['id'])

    async def delete():
        data = request.url_data
        return await Datum.delete(data['id'])

    async def update():
        data = json.loads(await request.body_data())
        did = data['id']
        data = data['data']
        return await Datum.update(did, data)

    return await {
        'POST': create,
        'GET': fetch,
        'PATCH': update,
        'DELETE': delete

    }[request.method]()


@wsgi.router('/data', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@jsonrpc
async def data(request: WsgiRequest) -> WsgiResponse:

    async def create():
        data = json.loads(await request.body_data())
        return await Data.create(**data)

    async def fetch():
        data = request.url_data
        return await Data.fetch(data['id'])

    async def delete():
        data = request.url_data
        return await Data.delete(data['id'])

    async def update():
        data = json.loads(await request.body_data())
        did = data['id']
        data = data['data']
        return await Data.update(did, data)

    return await {
        'POST': create,
        'GET': fetch,
        'PATCH': update,
        'DELETE': delete

    }[request.method]()
