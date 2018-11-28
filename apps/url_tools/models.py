# from datetime import datetime
#
# from django.db import models
# from django_mysql.models import JSONField, Model
#
# from scraper.models import BaseSpider
#
#
# class KeyWords(models.Model):
#     """
#     redis_key 可以在push的时候添加,没必要写到mysql数据库, 原本应该设计为树形结构,
#     但不考虑性能以及后期拓展, 所以简单粗暴了, crawl_key 字段需要自己单独合成或者进行处理！！
#     """
#     scraper = models.ForeignKey(BaseSpider, verbose_name="爬虫实例")
#     crawl_key = models.CharField(max_length=250, verbose_name="爬取关键字")
#     desc = models.TextField(blank=True, null=True, max_length=200, verbose_name="关键字说明")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "关键字列表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.crawl_key
#
#
# class ExcelLink(models.Model):
#     """
#     存储来自excel的链接
#     """
#     scraper = models.ForeignKey(BaseSpider, verbose_name="爬虫实例")
#     crawl_url = models.CharField(blank=True, null=True, max_length=255, verbose_name="爬取的url")
#     desc = models.TextField(blank=True, null=True, max_length=200, verbose_name="相关说明")
#     key_path = models.FileField(upload_to='files/ssh_key/%Y/%m', default='', blank=True, null=True,
#                                 max_length=200, verbose_name="文件上传")
#     # // models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图片")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "目标链接列表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.crawl_url
#
#
# class UrlManager(Model):
#     """
#     生成并推送链接到redis, redis相关配置请设定于django settings
#     """
#     name = models.CharField(max_length=100, verbose_name="链接推送管理", unique=True)
#     keywords = models.ForeignKey(KeyWords, verbose_name="目标关键字")  # 一个项目是否仅仅允许一个关键字
#     max_page = models.IntegerField(default=0, verbose_name="最大页码数")
#     url_template = models.CharField(default='', max_length=250, verbose_name="链接模板")
#     url_params = JSONField(blank=True, null=True, verbose_name="链接参数")
#     is_add_timestamp = models.BooleanField(default=False, verbose_name="是否添加时间戳")
#
#     check_cycle = models.IntegerField(default=5, verbose_name="检查周期")
#     lower_threshold = models.IntegerField(default=150, verbose_name="最小阈值")
#     upper_threshold = models.IntegerField(default=500, verbose_name="最大阈值")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "链接推送管理"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name



