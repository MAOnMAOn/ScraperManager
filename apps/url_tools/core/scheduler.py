import time
import logging
from multiprocessing import Process

from url_tools.core.redis_cli import RedisList
from url_tools.core.generator import UrlGenerator
from url_tools.core.config import (REDIS_KEY, BASE_URL_KEY, LOWER_THRESHOLD,
                                   UPPER_THRESHOLD, CHECK_CYCLE)

logger = logging.getLogger(__name__)


def get_keywords():
    return (item.decode("utf8") for item in RedisList().get_many(REDIS_KEY, 0, -1))


class UrlAdder(object):
    """
    just for scrapy_redis, default insert into redis list
    self.params = '%s:start_urls' % self.key  # for spider
    """
    def __init__(self, threshold):
        self._key = BASE_URL_KEY
        self._conn = RedisList(key=self._key)
        self._threshold = threshold
        self.key_set = get_keywords()  # it is a generator
        self.link_set = []
        self.num = 0

    def fetch_link_set(self, nums=300):
        key_list = []
        for key in self.key_set:
            key_list.append(key)
            if len(key_list) > nums:
                break
        self.link_set = UrlGenerator(key_list).get_link_set()

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('UrlAdder is working')
        while len(self.link_set) < 1:
            self.fetch_link_set()
        while not self.is_over_threshold() and len(self.link_set) > 0:
            url = self.link_set.pop()

            print('Add url into redis database: %s ' % url)
            self._conn.put(self._conn.params, url)

            if self.is_over_threshold():  # or url is None
                print('URL is enough, waiting to be used')
                self.num += 1
                print('Now add the %d th time' % self.num,
                      '\n',
                      'The number of remaining links is %d' % len(self.link_set))
                break
            if self._conn.queue_len == 0:
                raise Exception('ResourceDepletionError!')


class Schedule(object):

    @staticmethod
    def check_url(lower_threshold=LOWER_THRESHOLD,
                  upper_threshold=UPPER_THRESHOLD,
                  cycle=CHECK_CYCLE):
        """
        If the number of proxies less than lower_threshold, add proxy
        """
        conn = RedisList()
        adder = UrlAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    @staticmethod
    def run():
        insert_process = Process(target=Schedule.check_url)
        insert_process.start()
        insert_process.join()


def main():
    s = Schedule()
    try:
        s.run()
    except Exception as e:
        print(e)  # KeyError

