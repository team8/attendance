from django.db import models
from django.contrib import admin
import datetime

# Create your models here.

class UpdateAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		admin.ModelAdmin.save_model(self, request, obj, form, change)
		obj.save()

class Subteam(models.Model):
	name = models.CharField(max_length=25)
	averagePercentTimeWeighted = models.FloatField(default = 0)
	stddevPercentTimeWeighted = models.FloatField(default = 0)
	mostFrequentDay = models.CharField(max_length=25, default = "None")
	totalDaysWorked = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.name
		
	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)
		do_subteam_calcs(self)
		models.Model.save(self, *args, **kwargs)

class HoursWorked(models.Model): #This model should probably be renamed
	timeIn = models.DateTimeField() #Attribute that displays the time the student clocked in
	timeOut = models.DateTimeField() #Attribute that displays the time the student clocked out
	newTimeIn = models.DateTimeField(null=True, blank=True)
	newTimeOut = models.DateTimeField(null=True, blank=True)
	day = models.CharField(max_length=25, default="None") #Day that the hours happened
	totalTime = models.FloatField(default=0) #Attribute that...wait...this could be restructured a little bit, or at the very least renamed
	validTime = models.FloatField(default=0)
	autoLogout = models.BooleanField(default=False) #Boolean attribute that tells us if the entry was generated by our autoLogout script. In the future this will allow us to flag entries that were generated automatically and display them properly to our users
	outsideLabHours = models.BooleanField(default = False)
	percentTime = models.FloatField(default = 0)
	weight = models.FloatField(default = 0)
	owner = models.ForeignKey("Student")
	
	def __str__(self):
		return self.owner.name + ": " + self.timeIn.isoformat(' ')
	
	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)
		do_hours_worked_calcs(self)
		models.Model.save(self, *args, **kwargs)
		
class HoursWorkedEditSet(models.Model):
	owner = models.ForeignKey("Student")
	date = models.DateField()
	contents = models.ManyToManyField(HoursWorked, blank=True)
		
class AutoLogoutFilter(admin.SimpleListFilter):
	title = 'Auto Logout'
	parameter_name = 'auto_logout'
	
	def lookups(self, request, model_admin):
		return [
			('autoLogout', 'Auto Logout'),
			('autoLogoutCorrected', "Auto Logout + Corrected")
		]
	
	def queryset(self, request, queryset):
		if self.value() == 'autoLogout':
			return queryset.filter(totalTime__lt=60.0)
		elif self.value() == 'autoLogoutCorrected':
			return queryset.filter(totalTime__lt=60.0) | queryset.filter(autoLogout=True)
	
class HoursWorkedAdmin(UpdateAdmin):
	list_display = ('__str__', 'autoLogout', 'totalTime')
	list_filter = (AutoLogoutFilter, 'owner')

class Student(models.Model):
	name = models.CharField(max_length=50) #The student's name
	slackID = models.CharField(max_length=9, default = "None")
	studentID = models.IntegerField() #The student's ID#. In the future this may end up being a robotics ID#, if we decide to make custom ID cards
	subteam = models.ForeignKey(Subteam) #What subteam the student is associated with. There are a few fringe cases (most notably the team captain), we should decide how we want to handle those.
	hoursWorked = models.ManyToManyField(HoursWorked, blank=True)
	lastLoggedIn = models.DateTimeField(default = datetime.datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')) #Attribute that displays the last time this student logged in.
	atLab = models.BooleanField(default=False) #Boolean attribute that tells us if the student is at the lab.
	totalTime = models.FloatField(default=0)  #Attribute that...again, we need clarity on this one
	validTime = models.FloatField(default=0)
	
	averageTime = models.FloatField(default = 0) #average overall
	stddevTime = models.FloatField(default = 0) #stddev overall
	daysWorked = models.IntegerField(default = 0)
	percentDaysWorked = models.FloatField(default = 0) 
	averagePercentTimeWeighted = models.FloatField(default = 0) #weighted by length of lab hours
	stddevPercentTimeWeighted = models.FloatField(default = 0) #weighted by length of lab hours
	mostFrequentDay = models.CharField(max_length=25, default = "None")
	
	sudo = models.BooleanField(default=False) #determines whether user can sudo with attendance bot
	admin = models.BooleanField(default=False) #determines whether user can use admin privileges with attendance bot

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)
		do_student_calcs(self)
		models.Model.save(self, *args, **kwargs)

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

from attendanceapp.util import do_hours_worked_calcs, do_student_calcs, do_subteam_calcs