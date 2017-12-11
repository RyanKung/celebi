from pulsar.apps import MultiApp
from .measure import Measurement
from .entangle import Entanglement
from .monitor import Monitor

__all__ = [
    'Measurement',
    'Entanglement',
    'Monitor'
]


class ComposedAppTest(MultiApp):
    name = 'arbiters'

    def build(self):
        yield self.new_app(
            App=Monitor,
            name='pikachu_monitor',
            exchange_type='fanout',
            exchange='test',
            measurements=[Measurement()],
            entanglements=[Entanglement('test')],
            worker=3
        )

        yield self.new_app(
            App=Monitor,
            name='pikachu_monitor',
            exchange_type='fanout',
            exchange='test',
            measurements=[Measurement()],
            entanglements=[Entanglement('test')],
            worker=3
        )


class ComposedApp(MultiApp):
    name = 'celebi'

    def build(self):
        yield self.new_app(
            App=Monitor,
            name='pikachu_monitor',
            exchange_type='fanout',
            exchange='test',
            measurements=[Measurement()],
            entanglements=[Entanglement('test')],
            worker=3
        )
        yield self.new_app(ComposedAppTest)
