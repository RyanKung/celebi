# -*- eval: (venv-workon "celebi"); -*-

from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi, response

__all__ = ['meta']


@wsgi.router('/meta', methods=['GET'])
async def meta(request: WsgiRequest) -> WsgiResponse:
    return response({
    })
