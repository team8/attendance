# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0008_labhours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labhours',
            old_name='day',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='labhours',
            name='hours',
            field=models.DateTimeField(),
        ),
    ]
