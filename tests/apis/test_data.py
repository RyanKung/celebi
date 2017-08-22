from tests.apis import TestCelebiThread
import json


class TestMeta(TestCelebiThread):

    async def test_data(self):
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

    async def test_datum(self):
        self.assertEqual(1, 1)
