import redis

from url_tools.core.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):

        if password:
            self._db = redis.Redis(host=host, port=port, password=password)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, key):
        return self._db.get(key).decode('utf-8')

    def set(self, key, value):
        return self._db.set(key, value)

    def delete(self, keys):
        self._db.delete(keys)

    def type(self, keys):
        print(self._db.type(keys))

    def get_length(self, key):
        return self._db.llen(key)

    def keys(self, key):
        return self._db.keys(key)

    def exist(self, name):
        return self._db.exists(name)

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


class RedisList(RedisClient):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,
                 key=REDIS_KEY):
        super(RedisList, self).__init__(host=host, port=port, password=password)
        self.key = key
        self.params = '%s:start_urls' % self.key  # for spider

    def put(self, name, value):
        """
        add link to left top
        :param name:
        :param value:
        :return:
        """
        self._db.lpush(name, value)

    def get_one(self, name):
        """
        delete link to left top
        :return:link
        """
        value = self._db.lpop(name)
        return value

    def get_many(self, name, start, end):
        return self._db.lrange(name, start, end)

    @property
    def queue_len(self):
        """
        get length from queue and turn a method into a property call.
        """
        return self._db.llen(self.params)

