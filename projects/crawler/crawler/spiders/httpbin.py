# -*- coding: utf-8 -*-
import json
from random import uniform

import scrapy
from scrapy.http import Request

from ..items import SpiderInstanceItem, SpiderInstanceLoader


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']

    def start_requests(self):
        for i in range(800):
            url = 'http://httpbin.org/get' + "?param1=" + str(i)
            yield Request(url, callback=self.parse, meta={'url': url})

    def parse(self, response):
        data = SpiderInstanceLoader(item=SpiderInstanceItem(), response=response)
        data.add_value('spider', self.name)  # 这里是一个外键字段
        resp = json.loads(response.body_as_unicode())
        self.logger.info('This is my IP: %s' % resp['origin'])
        self.logger.info('This is my User-Agent: %s' % resp['headers']['User-Agent'])

        self.logger.debug('Status Code: ' + str(response.status))
        data.add_value('detail_url', response.url)
        data.add_value('title', uniform(100, 800))
        data.add_value('keyword', resp['origin'])
        yield data.load_item()
        # raise Exception("报错了!")


"""

"""