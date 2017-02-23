from unittest import TestCase
from app import main
from unittest.mock import patch, MagicMock, Mock
from app.database.db import DB

def from_url(a, **args):
    return mockRedis()

class mockRedis:

    def get(self, key):
        return key

    def keys(self, pattern):
        return  pattern

    def set(self, key, message):
        self.key = key
        self.message = message

    def lpush(self,key, message):
        self.key = key
        self.message = message

    def lrange(self, key, start, end):
        return ['mockList']

class TestDb(TestCase):

    @patch('app.database.db.redis.from_url')
    def test_get(self, mockRedis):
        mockRedis.side_effect = from_url

        db = DB()
        result = db.get('mockValue')
        self.assertEqual(result, 'mockValue', 'The result should be equal.')

        result = db.get_keys('pattern')
        self.assertEqual(result, 'pattern*', 'The result should be equal.')

        db.set(10, 'myMessage')
        self.assertEqual(db.db.key, 10, 'The key should be equal.')
        self.assertEqual(db.db.message, 'myMessage', 'The message should be equal.')

        db.push(11, 'myMessage')
        self.assertEqual(db.db.key, 11, 'The key should be equal.')
        self.assertEqual(db.db.message, 'myMessage', 'The message should be equal.')

        result = db.get_list('myKey')
        self.assertEqual(result, ['mockList'], 'The list should be equal.')
