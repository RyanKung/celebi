from pulsar.apps import ws
from pulsar import ensure_future
import logging
import json
from pulsar.apps.wsgi import route

__all__ = ['CelebiSocket']


class WebSocketRouter(ws.WebSocket):

    @route('/<int:qid>/', method='get')
    def qubit(self, request):
        qid = list(filter(bool, (request.path.split('/'))))[-1]
        request.qid = qid
        return super().get(request)


class PubSubWS(ws.WS):
    '''A :class:`.WS` handler with a publish-subscribe handler
    '''
    client = ws.PubSubClient

    def __init__(self):
        pass

    def on_open(self, websocket):
        qid = websocket.handshake.qid
        channel = self.channel % qid
        self.pubsub.add_client(self.client(websocket, channel))
        ensure_future(self.pubsub.subscribe(channel))
        logging.info(
            'New websocket opened. Add client to %s on "%s" channel',
            self.pubsub, self.channel)

    def write(self, websocket, message):
        data = json.loads(message)
        if not str(data['qid']) == str(websocket.handshake.qid):
            return
        logging.info('qid: %s, data %s' % (websocket.handshake.qid, data))
        websocket.write(data['data'])


CelebiSocket = WebSocketRouter(
    '/subscribe', PubSubWS())
