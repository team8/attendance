# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0014_labhours_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='lastLoggedIn',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 13, 0)),
        ),
    ]
