# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-21 12:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0006_auto_20180210_1226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crontabschedule',
            options={'ordering': ['month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute'], 'verbose_name': 'Crontab时间表', 'verbose_name_plural': 'Crontab时间表'},
        ),
        migrations.AlterModelOptions(
            name='intervalschedule',
            options={'ordering': ['period', 'every'], 'verbose_name': '时间间隔', 'verbose_name_plural': '时间间隔'},
        ),
        migrations.AlterModelOptions(
            name='periodictask',
            options={'verbose_name': '定时任务调度管理', 'verbose_name_plural': '定时任务调度管理'},
        ),
        migrations.AlterModelOptions(
            name='solarschedule',
            options={'ordering': ('event', 'latitude', 'longitude'), 'verbose_name': 'solar 事件', 'verbose_name_plural': 'solar 事件'},
        ),
    ]
