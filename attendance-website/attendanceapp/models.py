from django.db import models

# Create your models here.

class Subteam(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class HoursWorked(models.Model):
    timeIn = models.DateTimeField()
    timeOut = models.DateTimeField()
    totalTime = models.FloaFField()


class Student(models.Model):
    name = models.CharField(max_length=50)
    studentID = models.IntegerField()
    subteam = models.ForeignKey(Subteam)
    hoursWorked = models.ManyToManyField(HoursWorked)
    lastLoggedIn = models.DateTimeField()
    atLab = models.BooleanField(default=False)
    totalTime = models.FloatField()

    def __str__(self):
        return self.name
