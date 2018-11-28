# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy_djangoitem import DjangoItem

from scraper.models import BaseSpider, SpiderInstance, ECommerce


def select_spider(value):
    """ process foreign key """
    try:
        return BaseSpider.objects.get(name=value)
    except BaseSpider.DoesNotExist:
        return None


class SpiderInstanceItem(DjangoItem):
    django_model = SpiderInstance


class SpiderInstanceLoader(ItemLoader):
    # 继承ItemLoader, 重写output_processor,ItemLoader默认以list存放，选取默认字段可以修改output_processor
    default_output_processor = TakeFirst()  # 默认选取列表的第一项
    spider_in = MapCompose(select_spider)   # the foreign key field


class ECommerceItem(DjangoItem):
    django_model = ECommerce


class ECommerceLoader(SpiderInstanceLoader):
    pass


