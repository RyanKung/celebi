from tests.apis import TestCelebiThread


class TestMeta(TestCelebiThread):

    async def test_async_test(self):
        c = self.client
        url = self.uri + '/meta'
        response = await c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"result": [{}], "error": null, "id": 1}')

    def test_simple_test(self):
        self.assertEqual(1, 1)
