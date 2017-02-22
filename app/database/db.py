import redis
import os

class DB:
    def __init__(self):
        self.db = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

    def get(self, key):
        return self.db.get(key)

    def get_keys(self, pattern):
        return self.db.keys(pattern + '*')

    def set(self, key, message):
        self.db.set(key, message)

    def append(self, key, message):
        self.db.append(key, message)
