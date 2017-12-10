from django.db import models
from django.utils import timezone
import datetime
import pytz

# Create your models here.

class Subteam(models.Model):
    name = models.CharField(max_length=25)
    averagePercentTimeWeighted = models.FloatField(default = 0)
    stddevPercentTimeWeighted = models.FloatField(default = 0)
    mostFrequentDay = models.CharField(max_length=25, default = "None")
    totalDaysWorked = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name

class HoursWorked(models.Model): #This model should probably be renamed
    timeIn = models.DateTimeField() #Attribute that displays the time the student clocked in
    timeOut = models.DateTimeField(blank=True, null=True) #Attribute that displays the time the student clocked out
    day = models.CharField(max_length=25, default="None") #Day that the hours happened
    totalTime = models.FloatField(default=0) #Attribute that...wait...this could be restructured a little bit, or at the very least renamed
    autoLogout = models.BooleanField(default=False) #Boolean attribute that tells us if the entry was generated by our autoLogout script. In the future this will allow us to flag entries that were generated automatically and display them properly to our users
    outsideLabHours = models.BooleanField(default = False)
    weight = models.FloatField(default = 0)
    percentTime = models.FloatField(default = 0)

class Student(models.Model):
    name = models.CharField(max_length=50) #The student's name
    studentID = models.IntegerField() #The student's ID#. In the future this may end up being a robotics ID#, if we decide to make custom ID cards
    subteam = models.ForeignKey(Subteam) #What subteam the student is associated with. There are a few fringe cases (most notably the team captain), we should decide how we want to handle those.
    hoursWorked = models.ManyToManyField(HoursWorked, blank=True)
    lastLoggedIn = models.DateTimeField(default = datetime.datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')) #Attribute that displays the last time this student logged in.
    atLab = models.BooleanField(default=False) #Boolean attribute that tells us if the student is at the lab.
    totalTime = models.FloatField(default=0)  #Attribute that...again, we need clarity on this one
    averageTime = models.FloatField(default = 0) #average overall
    stddevTime = models.FloatField(default = 0) #stddev overall
    daysWorked = models.IntegerField(default = 0)
    percentDaysWorked = models.FloatField(default = 0) 
    averagePercentTimeWeighted = models.FloatField(default = 0) #weighted by length of lab hours
    stddevPercentTimeWeighted = models.FloatField(default = 0) #weighted by length of lab hours
    mostFrequentDay = models.CharField(max_length=25, default = "None")

    def __str__(self):
        return self.name

class LabHours(models.Model):
    name = models.CharField(default="None", max_length = 50)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    used = models.BooleanField(default = False)
    totalTime = models.FloatField(default = 0)
    
    def __str__(self):
        return self.name
    
class OverallStats(models.Model):
    name = models.CharField(default = "Overall Stats", max_length = 25)
    totalLabHours = models.FloatField()
    totalLabDays = models.IntegerField()