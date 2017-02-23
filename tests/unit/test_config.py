from unittest import TestCase
from app.config import Config


class TestConfig(TestCase):

    def test_getConfig(self):
        c = Config()
        c.config = 123
        result = c.get_config()

        self.assertEqual(result, 123, 'The result should be equal.')

    def test_getValue(self):
        c = Config()
        c.config = {'mySection': {'myKey': 'myValue'}}
        result = c.get_value('mySection', 'myKey')

        self.assertEqual(result, 'myValue', 'The result should be equal.')
