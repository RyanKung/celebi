from tests.apis import TestCelebiThread
import json
import datetime


class TestMeta(TestCelebiThread):

    async def test_data_first(self):
        c = self.client
        url = self.uri + '/data'
        response = await c.post(url, data=json.dumps(dict(name='test',
                                                          is_spout=False,
                                                          generator='',
                                                          comment='',
                                                          flying=True,
                                                          rate=1)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['result']['id'], 1)
        # get
        response = await c.get(url, params={'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['result']['id'], 1)
        # patch
        response = await c.patch(url, data=json.dumps({'id': 1, 'data': {'name': 'test2'}}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)
                         ['result'], [{'id': 1}])
        # get
        response = await c.get(url, params={'id': 1})
        self.assertEqual(json.loads(response.content)
                         ['result']['name'], 'test2')
        # delete
        response = await c.delete(url, params={'id': 1})
        self.assertEqual(response.status_code, 200)
        # get
        response = await c.get(url, params={'id': 1})
        self.assertEqual(json.loads(response.content)
                         ['result'], [])

        url = self.uri + '/data'
        response = await c.post(url, data=json.dumps(dict(name='test',
                                                          is_spout=False,
                                                          generator='',
                                                          comment='',
                                                          flying=True,
                                                          rate=1)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['result']['id'], 2)

    async def test_datume_next(self):
        # test datum
        c = self.client
        url = self.uri + '/datum'
        response = await c.post(url, data=json.dumps(dict(ts=str(datetime.datetime.now()),
                                                          dataset=2,
                                                          index='',
                                                          datum=json.dumps({
                                                              'datum': 'foo'}),
                                                          tags='none')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['result']['id'], 1)
