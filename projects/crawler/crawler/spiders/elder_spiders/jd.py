# # -*- coding: utf-8 -*-
# import json
# from urllib.parse import quote
# from datetime import datetime
#
# import scrapy
# from scrapy.http import Request
#
# from scrapy_module.items import ScrapyModuleItem, ScrapyModuleItemLoad
# from scrapy_module.settings import SQL_DATETIME_FORMAT
#
#
# class JdSpider(scrapy.Spider):
#     name = "jd"
#
#     def start_requests(self):
#         for i in range(1, 800):
#             url = "https://so.m.jd.com/ware/searchList.action?" \
#                   "keyword={key}&page={p}&_format_=json".format(key=quote('书'), p=str(i))
#             yield Request(url, callback=self.parse, meta={'url': url})  # errback=self.error_back,
#
#     def parse(self, response):
#         resp = json.loads(response.body_as_unicode())
#         keyword = ''  # response.meta['keyword']
#         try:
#             ware_list = json.loads(resp["value"])["wareList"]["wareList"]
#             if len(ware_list) > 0:
#                 for element in ware_list:
#                     # You need to let your ItemLoader work inside a specific selector, not response
#                     item_loader = ScrapyModuleItemLoad(item=ScrapyModuleItem(), selector=element)  # must put it here
#                     item_loader.add_value('name', self.name)
#                     item_loader.add_value('keyword', keyword)
#
#                     item_loader.add_value('location', '中国')
#                     item_loader.add_value('price', element['jdPrice'])
#                     item_loader.add_value('sold', element["totalCount"])
#                     item_loader.add_value('url', "http://item.m.jd.com/product/%s.html" % element["wareId"])
#                     item_loader.add_value('title', element["wname"].replace(',', '，'))
#                     item_loader.add_value('crawl_time', datetime.now().strftime(SQL_DATETIME_FORMAT))
#                     spider_item = item_loader.load_item()
#                     yield spider_item
#             else:
#                 print('******** Follow-up page no data, the crawl ended ********\n')
#         except KeyError:
#             pass


"""
class ScrapyModuleItemLoad(ItemLoader):
    # 继承ItemLoader, 重写output_processor,ItemLoader默认以list存放，选取默认字段可以修改output_processor 
    default_output_processor = TakeFirst()  # 默认选取列表的第一项

"""


    # def error_back(self, response):
    #     response = response.value.response
    #     item = ScrapyModuleItem()
    #
    #     item['name'] = self.name
    #     item['keyword'] = ''
    #     item['location'] = ''
    #     item['price'] = 0
    #     item['sold'] = 0
    #     item['url'] = response.request.meta['url']
    #     item['title'] = response.status
    #     item['crawl_time'] = datetime.now().strftime(SQL_DATETIME_FORMAT)
    #     yield item

