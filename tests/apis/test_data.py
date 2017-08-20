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
        self.assertEqual(response.content,
                         b'{"result": {}, "error": null, "id": 1}')

    async def test_data(self):
        self.assertEqual(1, 1)
