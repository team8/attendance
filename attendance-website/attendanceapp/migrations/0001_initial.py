# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayWorked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeIn', models.DateTimeField()),
                ('timeOut', models.DateTimeField()),
                ('totalTime', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('studentID', models.IntegerField()),
                ('daysWorked', models.ManyToManyField(to='attendanceapp.DayWorked')),
            ],
        ),
        migrations.CreateModel(
            name='Subteam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='subteam',
            field=models.ForeignKey(to='attendanceapp.Subteam'),
        ),
    ]
