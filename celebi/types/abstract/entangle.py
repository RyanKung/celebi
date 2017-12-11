import asyncio
import pika
from pulsar import send
from pulsar.async.consts import ACTOR_STATES


class Entanglement():
    name = 'test_entangle'
    rate = 1

    def __init__(
            self,
            exchange: str,
            *args,
            **kwargs
    ):
        self.exchange = exchange

    async def mapper(self, datum):
        return datum

    async def connect(self):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(exclusive=True).method.queue

    async def handler(self, channel, method, properties, body):
        await send(self.actor.monitor, 'fire', 'spout', body)

    async def entangle(self, actor, exc=None):
        await self.connect()
        self.channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue
        )
        # Check pika.adepter.process_data_events
        while actor.state is not ACTOR_STATES.STOPPING:
            await asyncio.sleep(self.rate)
            body: bytes = self.channel.basic_get(self.queue)[2]
            if not body:
                continue
            datum = await self.mapper(body.decode())
            await send(
                actor.monitor,
                'fire',
                'spout',
                data=datum
            )
        self.connection.close()
