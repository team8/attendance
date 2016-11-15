# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0007_hoursworked_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(default=b'None', max_length=25)),
                ('hours', models.TimeField(default=datetime.time(0, 0))),
            ],
        ),
    ]
