import re
import logging

from twisted.internet import task
from scrapy import signals

from . import connection, defaults


logger = logging.getLogger(__name__)


class SpeedStats(object):

    def __init__(self, server,
                 persist=False,
                 delete_on_start=False,
                 interval=60.0,
                 stats_key=defaults.STATS_KEY):
        """Initialize stats.

        Parameters
        ----------
        server : Redis
            The redis server instance.
        persist : bool
            Whether to flush requests when closing. Default is False.
        delete_on_start : bool
        stats_key:

        """
        self.server = server
        self.persist = persist
        self.delete_on_start = delete_on_start
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.stats_key = stats_key
        self.stats = None

    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'persist': settings.getbool('STATS_PERSIST'),
            'delete_on_start': settings.getbool('STATS_DELETE_ON_START'),
            'interval': settings.getfloat('LOGSTATS_INTERVAL')
        }

        server = connection.from_settings(settings)
        return cls(server=server, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(instance.spider_closed, signal=signals.spider_closed)
        return instance

    def spider_opened(self, spider):
        self.pagesprev = 0
        self.itemsprev = 0

        self.redis_key = self.stats_key % {'spider': spider.name}
        self.exists(spider)

        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        spider_items = self.stats.get_value('item_scraped_count', 0)
        spider_pages = self.stats.get_value('response_received_count', 0)
        items = float(self.get_stats(spider)[0]) + spider_items - self.itemsprev
        pages = float(self.get_stats(spider)[2]) + spider_pages - self.pagesprev
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier

        self.pagesprev, self.itemsprev = pages, items

        self.push(items, pages, irate, prate, spider)

        msg = ("Crawled %(pages)d pages (at %(pagerate)d pages/min), "
               "scraped %(items)d items (at %(itemrate)d items/min)")
        log_args = {'pages': pages, 'pagerate': prate,
                    'items': items, 'itemrate': irate}
        logger.info(msg, log_args, extra={'spider': spider})

        if self.delete_on_start:
            self.delete_key(self.redis_key)

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
        if self.persist:
            self.delete_key(self.redis_key)

    def delete_key(self, key):
        self.server.delete(key)

    def push(self, items, irate, pages, prate, spider):
        stator = "{}pages{}pages/min{}items{}items/min".format(items, irate, pages, prate)
        self.server.lpush(self.redis_key, stator)

    def get_stats(self, spider):
        key = self.server.lrange(self.redis_key, -2, -1)[0].decode('utf-8')
        return [i for i in re.split('[a-z]|/', key) if len(i) > 0]

    def exists(self, spider):
        if not self.server.exists(self.redis_key):
            self.push(0, 0, 0, 0, spider)
