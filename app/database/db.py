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

    def push(self, key, message):
        self.db.lpush(key, message)

    def get_list(self, key, start=0, end=-1):
        return self.db.lrange(key, start, end)
