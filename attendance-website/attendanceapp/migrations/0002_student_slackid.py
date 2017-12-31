# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='slackID',
            field=models.CharField(default=b'None', max_length=9),
        ),
    ]
