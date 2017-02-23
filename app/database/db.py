import redis
import os
from app import logger


class DB:
    """
    This class is responsible for handling the Data Base
    """
    def __init__(self):
        """
        Starts a DB instance
        """

        self.db = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

    def get(self, key):
        """
        return the value of key
        """
        logger.debug('db get key: ' + str(key) + ' value: ' + str(self.db.get(key)))
        return self.db.get(key)

    def get_keys(self, pattern):
        """
        return keys that match a pattern
        """
        logger.debug('get keys by pattern: ' + str(pattern))
        return self.db.keys(pattern + '*')

    def set(self, key, message):
        """
        set message for a key
        """
        logger.debug('set key: ' + str(key) + ' with value: ' + str(message))
        self.db.set(key, message)

    def push(self, key, message):
        """
        append message to a key
        """
        logger.debug('push key: ' + str(key) + ' value: ' + str(message))
        self.db.lpush(key, message)

    def get_list(self, key, start=0, end=-1):
        """
        return the a list for a specific key
        """
        logger.debug('get a list, key: ' + str(key))
        return self.db.lrange(key, start, end)
