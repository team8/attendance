# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0006_auto_20151029_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoursworked',
            name='day',
            field=models.CharField(default=b'None', max_length=25),
        ),
    ]
