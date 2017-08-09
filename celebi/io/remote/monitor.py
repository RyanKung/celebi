import aio_etcd as etcd
from pulsar.apps.wsgi import WSGIServer, WsgiResponse
from celebi.io.abstract import CelebiMonitor
from pulsar.apps.wsgi import Router

__all__ = ['RemoteMonitorWSGI']

blueprint = Router('/')


@blueprint.router('/', methods=['post'])
def remote_wsgi(request):
    return WsgiResponse('test')


class RemoteMonitorWSGI(WSGIServer, CelebiMonitor):
    name = 'remote_monitor'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg.callable = blueprint

    async def monitor_start(self, monitor, exec=None):
        if not hasattr(self.cfg, 'etcdconf'):
            monitor.etcd = etcd.Client()
        else:
            monitor.etcd = etcd.Client(**self.cfg.etcdconf)
        await super().monitor_start(monitor)
