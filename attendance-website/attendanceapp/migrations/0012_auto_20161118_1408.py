# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0011_auto_20161117_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='labhours',
            name='totalTime',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='overallstats',
            name='name',
            field=models.CharField(default=b'Overall Stats', max_length=25),
        ),
    ]
