# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0002_auto_20151022_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hoursWorked',
            field=models.ManyToManyField(to='attendanceapp.HoursWorked', null=True),
        ),
    ]
