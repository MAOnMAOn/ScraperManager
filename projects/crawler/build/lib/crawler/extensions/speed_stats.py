# -*- coding:utf-8 _*-

"""
@author: maonmaon
@time: 2018/09/18
@contact: 958093654@qq.com
"""
import socket
import logging

from redis import StrictRedis, ConnectionPool
from twisted.internet import task
from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class LogStats(object):

    def __init__(self, stats, bot_name, redis_url, interval=60.0,
                 delete_on_start=True, persist=False):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.task = None
        self.redis_url = redis_url
        self.bot_name = bot_name
        self.delete_on_start = delete_on_start
        self.persist = persist
        self._con = self.get_connection(self.redis_url)

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        delete_on_start = crawler.settings.getbool('STATS_DELETE_ON_START')
        persist = crawler.settings.getbool('STATS_PERSIST')
        redis_url = crawler.settings.get('REDIS_URL', 'redis://root:foobared@192.168.2.58:6379')
        bot_name = crawler.settings.get('BOT_NAME')
        o = cls(crawler.stats, bot_name, redis_url, interval, delete_on_start, persist)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    @staticmethod
    def get_connection(redis_url):
        pool = ConnectionPool.from_url(redis_url)
        con = StrictRedis(connection_pool=pool)
        return con

    def spider_opened(self, spider):
        self.pagesprev = 0
        self.itemsprev = 0

        self.key = self.bot_name + "_" + spider.name + ':' + str(
            socket.gethostname()) + "_" + get_host_ip()
        if self.delete_on_start:
            self.delete_key(self.key)
        self.exists(self.key)

        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        items = self.stats.get_value('item_scraped_count', 0)
        pages = self.stats.get_value('response_received_count', 0)
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier
        self.pagesprev, self.itemsprev = pages, items

        msg = ("Crawled %(pages)d pages (at %(pagerate)d pages/min), "
               "scraped %(items)d items (at %(itemrate)d items/min)")
        log_args = {'pages': pages, 'pagerate': prate,
                    'items': items, 'itemrate': irate}
        logger.info(msg, log_args, extra={'spider': spider})

        self.push(items=items, irate=irate, pages=pages, prate=prate, spider=spider)

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()

        if self.persist:
            self.delete_key(self.key)

    def delete_key(self, key):
        self._con.delete(key)

    def push(self, items, irate, pages, prate, spider):
        stator = "{}pages{}pages/min{}items{}items/min".format(items, irate, pages, prate)
        self._con.lpush(self.key, stator)

    def exists(self, spider):
        if not self._con.exists(self.key):
            self.push(0, 0.0, 0, 0.0, spider)
