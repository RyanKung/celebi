from typing import Union, Callable
from types import CoroutineType
from pulsar.apps.wsgi import WsgiResponse, WsgiRequest

__all__ = ['Request', 'Response', 'MaybeCorouteine', 'Handler']


Request = WsgiRequest
Response = WsgiResponse
MaybeCorouteine = Union[CoroutineType, Callable]
Handler = Callable[..., WsgiResponse]
