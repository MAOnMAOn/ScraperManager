# -*- coding:utf-8 _*-

"""
@author: maonmaon
@time: 2018/09/14
@contact: 958093654@qq.com
"""
from datetime import datetime

from django.db import models
from django_mysql.models import JSONField, Model


class Project(models.Model):
    name = models.CharField(max_length=60, verbose_name="项目名称" , unique=True)
    desc = models.TextField(null=True, blank=True, verbose_name="项目说明")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name  # 这样可以直接 list_display


class BaseSpider(Model):
    name = models.CharField(max_length=60, verbose_name="爬虫名称")
    project = models.ForeignKey(Project, verbose_name="项目名称")
    website = models.CharField(max_length=60, blank=True, null=True, default='', verbose_name="网站")
    desc = models.TextField(null=True, blank=True, verbose_name="爬虫说明")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = '爬虫基类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SpiderInstance(Model):
    spider = models.ForeignKey(BaseSpider, verbose_name="爬虫名称")
    title = models.CharField(max_length=200, blank=True, null=True, default='', verbose_name="详情页标题")
    keyword = models.CharField(max_length=120, blank=True, null=True, default='', verbose_name="关键字")
    detail_url = models.CharField(max_length=253, blank=True, null=True, default='', verbose_name="详情页链接")
    scraper_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")
    supplement = JSONField(blank=True, null=True, verbose_name="补充字段")
    version = models.DateField(auto_now=True, verbose_name="版本日期")

    class Meta:
        verbose_name = '实例爬虫'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '实例爬虫'


class ECommerce(SpiderInstance):
    price = models.CharField(max_length=60, blank=True, null=True, default='', verbose_name="商品价格")
    sold = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name="销量")
    location = models.CharField(max_length=100, blank=True, null=True, default='中国', verbose_name="地区")

    class Meta:
        verbose_name = '电商爬虫'
        verbose_name_plural = verbose_name
