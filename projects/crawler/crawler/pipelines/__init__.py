from .mysql import MySQLPipeline
from .mongo import MongoPipeline


class CrawlerPipeline(object):
    """ just for django item data storage """
    def process_item(self, item, spider):
        item.save()
        return item
