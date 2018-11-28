# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-21 07:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url_tools', '0008_auto_20181121_1521'),
        ('scraper', '0004_auto_20181024_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basespider',
            name='project',
        ),
        migrations.RemoveField(
            model_name='ecommerce',
            name='spiderinstance_ptr',
        ),
        migrations.RemoveField(
            model_name='spiderinstance',
            name='spider',
        ),
        migrations.DeleteModel(
            name='BaseSpider',
        ),
        migrations.DeleteModel(
            name='ECommerce',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='SpiderInstance',
        ),
    ]