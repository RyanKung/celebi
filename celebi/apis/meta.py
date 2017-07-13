# -*- eval: (venv-workon "celebi"); -*-

from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi
from celebi.core.decorators import jsonrpc

__all__ = ['meta']


@wsgi.router('/meta', methods=['GET'])
@jsonrpc
async def meta(request: WsgiRequest) -> WsgiResponse:
    return {
    }
