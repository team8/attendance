# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-17 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0006_hoursworkededit_hoursworkededitset'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoursworkededit',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendanceapp.Student'),
            preserve_default=False,
        ),
    ]
