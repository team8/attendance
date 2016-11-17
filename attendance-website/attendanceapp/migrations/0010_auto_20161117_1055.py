# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0009_auto_20161115_1939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labhours',
            old_name='hours',
            new_name='endtime',
        ),
        migrations.AddField(
            model_name='hoursworked',
            name='outsideLabHours',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='labhours',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 17, 18, 55, 24, 967043, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
