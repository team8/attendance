# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0003_auto_20180101_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subteam',
            name='averagePercentTimeWeighted',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='subteam',
            name='stddevPercentTimeWeighted',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]