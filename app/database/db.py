import redis
import os
from app import logger

class DB:
    def __init__(self):

        self.db = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
        #self.db = redis.from_url('localhost', decode_responses=True)

    def get(self, key):
        logger.debug('db get key: ' + str(key) + ' value: ' + str(self.db.get(key)))
        return self.db.get(key)

    def get_keys(self, pattern):
        logger.debug('get keys by pattern: ' + str(pattern))
        return self.db.keys(pattern + '*')

    def set(self, key, message):
        logger.debug('set key: ' + str(key) + ' with value: ' + str(message))
        self.db.set(key, message)

    def push(self, key, message):
        logger.debug('push key: '+ str(key) + ' value: ' + str(message))
        self.db.lpush(key, message)

    def get_list(self, key, start=0, end=-1):
        logger.debug('get a list, key: ' + str(key))
        return self.db.lrange(key, start, end)
