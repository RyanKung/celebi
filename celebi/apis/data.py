# -*- eval: (venv-workon "celebi"); -*-

from pulsar.apps.wsgi import WsgiResponse, WsgiRequest
from celebi.core.wsgi import wsgi, response

__all__ = ['datum']


@wsgi.router('/auth', methods=['GET', 'POST'])
async def datum(request: WsgiRequest) -> WsgiResponse:
    return response('test')
