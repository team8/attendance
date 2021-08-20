from django.db import models


class SubTeam(models.Model):
    name = models.CharField(max_length=25)
    averagePercentTimeWeighted = models.FloatField(default=0)
    stddevPercentTimeWeighted = models.FloatField(default=0)
    mostFrequentDay = models.CharField(max_length=25, default="None")
    totalDaysWorked = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class WorkTime(models.Model):
    timeIn = models.DateTimeField()  # Time the student logged in
    timeOut = models.DateTimeField()  # Time the student logged out
    newTimeIn = models.DateTimeField(null=True, blank=True)
    newTimeOut = models.DateTimeField(null=True, blank=True)
    day = models.CharField(max_length=25, default="None")  # Day the hours happened
    totalTime = models.FloatField(default=0)  # Total time the person stayed at lab today
    validTime = models.FloatField(default=0)  # Time stayed at lab while it is open
    autoLogout = models.BooleanField(default=False)  # If the person was auto logged out
    outsideLabHours = models.BooleanField(default=False)
    percentTime = models.FloatField(default=0)  # Percent of the total lab time
    weight = models.FloatField(default=0)
    owner = models.ForeignKey("Student", on_delete=models.CASCADE)  # Who these hours have been worked by


class Student(models.Model):
    name = models.CharField(max_length=50)  # Name of the student
    slackID = models.CharField(max_length=9, default="None")  # IDK if we are using this
    studentID = models.IntegerField()  # 950 number
    subTeam = models.ForeignKey(SubTeam, on_delete=models.PROTECT)
    hoursWorked = models.ManyToManyField(WorkTime, blank=True)  # Total hours worked throughout the season
    validTime = models.FloatField(default=0)  # Total valid hours worked throughout the season

    averageTime = models.FloatField(default=0)
    stddevTime = models.FloatField(default=0)
    daysWorked = models.IntegerField(default=0)
    percentDaysWorked = models.FloatField(default=0)
    averagePercentTimeWeighted = models.FloatField(default=0)  # weighted by length of lab hours
    stddevPercentTimeWeighted = models.FloatField(default=0)  # weighted by length of lab hours
    mostFrequentDay = models.CharField(max_length=25, default="None")

    def __str__(self):
        return self.name


class LabHours(models.Model):
    name = models.CharField(default="None", max_length=50)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    used = models.BooleanField(default=False)
    totalTime = models.FloatField(default=0)


class OverallStats(models.Model):
    name = models.CharField(default="Overall Stats", max_length=25)
    totalLabHours = models.FloatField()
    totalLabDays = models.IntegerField()

# Create your models here.
