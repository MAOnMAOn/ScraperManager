# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-12 03:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploy',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployment.Client', verbose_name='Scrapyd客户端'),
        ),
        migrations.AlterField(
            model_name='deploy',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployment.Project', verbose_name='项目名称'),
        ),
    ]
