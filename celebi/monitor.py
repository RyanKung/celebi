import pika
import json
from pulsar.apps import Application
from .entangle import Entanglement
from .measure import Measurement
from pulsar import command
from pulsar.async.consts import ACTOR_STATES


@command(ack=False)
async def fire(request, event, **kw):
    if request.actor.state is not ACTOR_STATES.STOPPING:
        request.actor.fire_event(event, **kw)


class Monitor(Application):
    def __init__(
            self,
            # name: str,
            # exchange: str,
            # exchange_type: str,
            # entanglements=[],
            # measurements=[],
            cfg,
            *args,
            **kwargs
    ):

        self.name = cfg.name
        self.exchange: str = cfg.exchange
        self.exchange_type: str = cfg.exchange_type
        self._measurements = cfg.measurements
        self._measuring = []
        self._entanglements = cfg.entanglements
        self._entangleing = []
        super().__init__(cfg=cfg, *args, **kwargs)

    def spout(
            self,
            monitor,
            data,
            **kwargs
    ):
        assert self.channel.basic_publish(
            exchange=self.exchange,
            routing_key='',
            body=json.dumps(data)
        )
        return

    def connect_channel(self):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type
        )

    async def monitor_start(self, monitor, exc=None):
        monitor.bind_event('spout', self.spout)
        self.connect_channel()
        self._measuring: list = [
            self.spawn_measuring_actor(monitor, m)
            for m in self._measurements
        ]
        self._entangling: list = [
            self.spawn_entangling_actor(monitor, e)
            for e in self._entanglements
        ]

    async def monitor_stopping(self, monitor, exc=None):
        self.connection.close()

    def spawn_measuring_actor(self, monitor, m: Measurement):
        actor = monitor.spawn(
            name=m.name,
            start=m.measure
        )
        return actor

    def spawn_entangling_actor(self, monitor, e: Entanglement):
        actor = monitor.spawn(
            name=e.name,
            start=e.entangle
        )
        return actor

    def measure(self, m: Measurement):
        self._measurements.append(m)

    def entangle(self, e: Entanglement):
        self._entanglements.append(e)
