import aio_etcd as etcd
from pulsar import get_actor
from pulsar.apps.wsgi import WSGIServer, WsgiResponse, WsgiHandler
from celebi.io.abstract import CelebiMonitor
from pulsar.apps.wsgi import Router

__all__ = ['RemoteMonitorWSGI']

blueprint = Router('/')


@blueprint.router('/remote/<string:monitor>/', methods=['post'])
async def remote_wsgi(request):
    monitor = request.urlargs['monitor']
    actor = get_actor()
    print(actor.is_arbiter(), actor.is_monitor(), actor.name)
    monitor = actor.get_actor('remote_monitor')
    if monitor:
        monitor.fire_event('test', 'fukcing run')
    elif not (actor.is_arbiter() or actor.is_monitor()):
        actor.monitor.fire_event('test', s='fukcing run')
    else:
        print('cant find monitor')
    return WsgiResponse(200, 'test')


class RemoteMonitorWSGI(WSGIServer, CelebiMonitor):
    name = 'remote_monitor'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg.callable = WsgiHandler((blueprint, ))
        if not hasattr(self.cfg, 'blacklist'):
            self.cfg.blacklist = []

    @staticmethod
    def event_test(s):
        print('test event %s' % s)

    async def monitor_start(self, monitor, exec=None):
        monitor.bind_event('test', self.event_test)
        if not hasattr(self.cfg, 'etcdconf'):
            monitor.etcd = etcd.Client()
        else:
            monitor.etcd = etcd.Client(**self.cfg.etcdconf)
        await super().monitor_start(monitor)

    async def worker_start(self, worker, *args, **kwargs):
        worker.bind_event('test', self.event_test)
