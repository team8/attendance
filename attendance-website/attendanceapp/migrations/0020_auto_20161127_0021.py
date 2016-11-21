# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0019_auto_20161121_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mostAttendedDay', models.CharField(default=b'None', max_length=25)),
                ('averageTime', models.FloatField(default=0)),
                ('stddevTime', models.FloatField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='labhours',
            name='name',
            field=models.CharField(default=b'None', max_length=50),
        ),
    ]
