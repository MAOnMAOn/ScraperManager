# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-24 01:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20181024_0934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basespider',
            options={'verbose_name': '爬虫创建', 'verbose_name_plural': '爬虫创建'},
        ),
        migrations.AlterModelOptions(
            name='ecommerce',
            options={'verbose_name': '爬虫实例数据(电商)', 'verbose_name_plural': '爬虫实例数据(电商)'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '项目创建', 'verbose_name_plural': '项目创建'},
        ),
        migrations.AlterModelOptions(
            name='spiderinstance',
            options={'verbose_name': '爬虫实例数据', 'verbose_name_plural': '爬虫实例数据'},
        ),
    ]
