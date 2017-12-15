import asyncio
import pika
from pika.connection import URLParameters
from pulsar import send
from pulsar.async.consts import ACTOR_STATES
from celebi.utils import retry


class Entanglement():

    def __init__(
            self,
            name: str,
            rate: int,
            exchange: str,
            amqp_url,
            mapper=lambda x: x,
            *args,
            **kwargs
    ):
        self.name = name
        self.rate = rate
        self.exchange = exchange
        self.amqp_url = amqp_url

    async def mapper(self, datum):
        return datum

    @retry
    async def connect(self):
        url = URLParameters(self.amqp_url)
        self.connection = pika.BlockingConnection(url)
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
