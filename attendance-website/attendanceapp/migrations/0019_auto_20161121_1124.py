# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0018_auto_20161121_1000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='mostFequentDay',
            new_name='mostFrequentDay',
        ),
    ]
