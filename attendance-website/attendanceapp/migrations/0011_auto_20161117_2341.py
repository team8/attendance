# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0010_auto_20161117_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='OverallStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('totalLabHours', models.FloatField()),
                ('totalLabDays', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='hoursworked',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='averagePercentTimeWeighted',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='averageTime',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='student',
            name='daysWorked',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='mostFequentDay',
            field=models.CharField(default=b'None', max_length=25),
        ),
        migrations.AddField(
            model_name='student',
            name='percentDaysWorked',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='stddevPercentTimeWeighted',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='stddevTime',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='subteam',
            name='averageTime',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
