from tests.apis import TestCelebiThread


class MyTest(TestCelebiThread):

    async def test_async_test(self):
        pass

    def test_simple_test(self):
        self.assertEqual(1, 1)
