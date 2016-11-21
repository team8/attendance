# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0015_auto_20161119_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='lastLoggedIn',
        ),
    ]
