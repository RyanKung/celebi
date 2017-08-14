from tests.apis import TestCelebiThread


class TestMeta(TestCelebiThread):

    async def test_datum(self):
        c = self.client
        url = self.uri + '/datum'
        response = await c.post(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b'{"result": {}, "error": null, "id": 1}')

    async def test_data(self):
        self.assertEqual(1, 1)
