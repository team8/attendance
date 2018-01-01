# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0002_student_slackid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoursworked',
            name='timeOut',
            field=models.DateTimeField(),
        ),
    ]
