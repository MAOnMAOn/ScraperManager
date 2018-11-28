# -*- coding: utf-8 -*-
import re
import json

import scrapy
import pandas as pd
from scrapy.http import Request

from ..items import ECommerceItem, ECommerceLoader


class DemoSpider(scrapy.Spider):
    name = 'demo'
    # custom_settings = {
    #     "DOWNLOAD_DELAY": 1,
    # }

    def start_requests(self):
        for page in range(6, 7):
            url = 'https://m.hc360.com/prod-mhf/900184063-{page}.html'.format(page=page)
            yield Request(url, callback=self.parse, meta={"keyword": "塑料托盘"}, dont_filter=True)
        for page in range(6, 7):
            url = 'https://m.hc360.com/prod-0/900108055-{page}.html'.format(page=page)
            yield Request(url, callback=self.parse, meta={"keyword": "金属托盘"}, dont_filter=True)

    def parse(self, response):
        for item in response.xpath('/html/body/section[1]/article[@class="fListBox"]/ul/li'):
            url = "https:" + item.xpath('./div[1]/span/a/@href').extract()[0]
            keyword = response.meta['keyword']
            yield Request(url, callback=self.parse_detail, meta={"keyword": keyword})

    def parse_detail(self, response):
        data = ECommerceLoader(item=ECommerceItem(), response=response)
        data.add_value('spider', self.name)  # 这里是一个外键字段
        data.add_xpath('title', '//h1/text()')
        price = response.xpath('/html/body/section[1]/section[1]/article/div[2]/p[1]').xpath('string(.)').extract()[0]
        data.add_value('price', re.sub("\r|\n|\\s|", "", price).split('-')[0].replace('¥', ''))
        data.add_value('detail_url', response.url)
        data.add_value('keyword', response.meta['keyword'])
        supplement = pd.read_html(response.text)[0].to_dict(orient='split')['data']
        json_dict = dict()
        for i in supplement:
            if re.search('材质', i[0]):
                json_dict['material'] = i[-1]
            if re.search('尺寸', i[0]):
                json_dict['size'] = i[-1]
        if json_dict:
            data.add_value('supplement', json.dumps(json_dict, ensure_ascii=False))
        yield data.load_item()


