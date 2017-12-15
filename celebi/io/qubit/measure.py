from pulsar.async.consts import ACTOR_STATES
from pulsar import send
import asyncio
from celebi.core.types import MaybeAsyncCallable
from asyncio import iscoroutinefunction


class Measurement():

    def __init__(
            self,
            name,
            spout: MaybeAsyncCallable,
            rate: int
    ):
        self.name = name
        self.spout = spout
        self.rate = rate

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(self.rate)
        if iscoroutinefunction(self.spout):
            return await self.spout()
        else:
            return self.spout()

    async def measure(self, actor, exc=None):
        async for datum in self:
            if actor.state is ACTOR_STATES.STOPPING:
                return
            await send(
                actor.monitor,
                'fire',
                'spout',
                data=datum
            )
