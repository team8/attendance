# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0020_auto_20161127_0021'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TeamStats',
        ),
    ]
