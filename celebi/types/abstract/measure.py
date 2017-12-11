from pulsar.async.consts import ACTOR_STATES
from pulsar import send
import asyncio


class Measurement():

    name = 'test_measure'
    rate = 1

    async def fetch(self):
        return {
            'hello': 'world'
        }

    async def mapper(self, datum: dict):
        datum.update({'world': 'hello'})
        return datum

    async def measure(self, actor, exc=None):
        while actor.state is not ACTOR_STATES.STOPPING:
            await asyncio.sleep(self.rate)
            datum = await self.mapper(
                await self.fetch()
            )
            await send(
                actor.monitor,
                'fire',
                'spout',
                data=datum
            )
