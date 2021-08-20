# Generated by Django 3.2.6 on 2021-08-20 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=50)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('totalTime', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OverallStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Overall Stats', max_length=25)),
                ('totalLabHours', models.FloatField()),
                ('totalLabDays', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slackID', models.CharField(default='None', max_length=9)),
                ('studentID', models.IntegerField()),
                ('validTime', models.FloatField(default=0)),
                ('averageTime', models.FloatField(default=0)),
                ('stddevTime', models.FloatField(default=0)),
                ('daysWorked', models.IntegerField(default=0)),
                ('percentDaysWorked', models.FloatField(default=0)),
                ('averagePercentTimeWeighted', models.FloatField(default=0)),
                ('stddevPercentTimeWeighted', models.FloatField(default=0)),
                ('mostFrequentDay', models.CharField(default='None', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='SubTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('averagePercentTimeWeighted', models.FloatField(default=0)),
                ('stddevPercentTimeWeighted', models.FloatField(default=0)),
                ('mostFrequentDay', models.CharField(default='None', max_length=25)),
                ('totalDaysWorked', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeIn', models.DateTimeField()),
                ('timeOut', models.DateTimeField()),
                ('newTimeIn', models.DateTimeField(blank=True, null=True)),
                ('newTimeOut', models.DateTimeField(blank=True, null=True)),
                ('day', models.CharField(default='None', max_length=25)),
                ('totalTime', models.FloatField(default=0)),
                ('validTime', models.FloatField(default=0)),
                ('autoLogout', models.BooleanField(default=False)),
                ('outsideLabHours', models.BooleanField(default=False)),
                ('percentTime', models.FloatField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendanceapp.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='hoursWorked',
            field=models.ManyToManyField(blank=True, to='attendanceapp.WorkTime'),
        ),
        migrations.AddField(
            model_name='student',
            name='subTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendanceapp.subteam'),
        ),
    ]