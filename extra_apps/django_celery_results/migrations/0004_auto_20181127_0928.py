# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-27 01:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0003_auto_20181106_1101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskresult',
            options={'ordering': ['-date_done'], 'verbose_name': '任务结果', 'verbose_name_plural': '任务结果'},
        ),
    ]
