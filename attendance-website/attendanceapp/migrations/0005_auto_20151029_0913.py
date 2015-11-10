# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0004_auto_20151022_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoursworked',
            name='autoLogout',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hoursworked',
            name='timeOut',
            field=models.DateTimeField(blank=True),
        ),
    ]
