# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HoursWorked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeIn', models.DateTimeField()),
                ('timeOut', models.DateTimeField(null=True, blank=True)),
                ('day', models.CharField(default=b'None', max_length=25)),
                ('totalTime', models.FloatField(default=0)),
                ('validTime', models.FloatField(default=0)),
                ('autoLogout', models.BooleanField(default=False)),
                ('outsideLabHours', models.BooleanField(default=False)),
                ('percentTime', models.FloatField(default=0)),
                ('weight', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LabHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'None', max_length=50)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('totalTime', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OverallStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Overall Stats', max_length=25)),
                ('totalLabHours', models.FloatField()),
                ('totalLabDays', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('studentID', models.IntegerField()),
                ('lastLoggedIn', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('atLab', models.BooleanField(default=False)),
                ('totalTime', models.FloatField(default=0)),
                ('validTime', models.FloatField(default=0)),
                ('averageTime', models.FloatField(default=0)),
                ('stddevTime', models.FloatField(default=0)),
                ('daysWorked', models.IntegerField(default=0)),
                ('percentDaysWorked', models.FloatField(default=0)),
                ('averagePercentTimeWeighted', models.FloatField(default=0)),
                ('stddevPercentTimeWeighted', models.FloatField(default=0)),
                ('mostFrequentDay', models.CharField(default=b'None', max_length=25)),
                ('hoursWorked', models.ManyToManyField(to='attendanceapp.HoursWorked', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subteam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('averagePercentTimeWeighted', models.FloatField(default=0)),
                ('stddevPercentTimeWeighted', models.FloatField(default=0)),
                ('mostFrequentDay', models.CharField(default=b'None', max_length=25)),
                ('totalDaysWorked', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='subteam',
            field=models.ForeignKey(to='attendanceapp.Subteam'),
        ),
        migrations.AddField(
            model_name='hoursworked',
            name='owner',
            field=models.ForeignKey(to='attendanceapp.Student'),
        ),
    ]
