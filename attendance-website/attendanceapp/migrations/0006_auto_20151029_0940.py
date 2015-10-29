# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0005_auto_20151029_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoursworked',
            name='timeOut',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
