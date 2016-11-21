# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0012_auto_20161118_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subteam',
            name='averageTime',
        ),
        migrations.AddField(
            model_name='hoursworked',
            name='percentTime',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='subteam',
            name='averagePercentTimeWeighted',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='subteam',
            name='mostFrequentDay',
            field=models.CharField(default=b'None', max_length=25),
        ),
        migrations.AddField(
            model_name='subteam',
            name='stddevPercentTimeWeighted',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='subteam',
            name='totalDaysWorked',
            field=models.IntegerField(default=0),
        ),
    ]
