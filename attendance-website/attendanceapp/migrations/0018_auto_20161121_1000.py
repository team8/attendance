# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0017_student_lastloggedin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='lastLoggedIn',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0, tzinfo=utc)),
        ),
    ]
