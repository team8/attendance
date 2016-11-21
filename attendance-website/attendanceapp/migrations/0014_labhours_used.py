# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0013_auto_20161119_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='labhours',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
