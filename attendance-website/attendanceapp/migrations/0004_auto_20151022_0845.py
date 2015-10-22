# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0003_auto_20151022_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hoursWorked',
            field=models.ManyToManyField(to='attendanceapp.HoursWorked', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='lastLoggedIn',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
