# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoursWorked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeIn', models.DateTimeField()),
                ('timeOut', models.DateTimeField()),
                ('totalTime', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='daysWorked',
        ),
        migrations.AddField(
            model_name='student',
            name='atLab',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='lastLoggedIn',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='totalTime',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='DayWorked',
        ),
        migrations.AddField(
            model_name='student',
            name='hoursWorked',
            field=models.ManyToManyField(to='attendanceapp.HoursWorked'),
        ),
    ]
