from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Subteam, LabHours, Student, HoursWorked
from attendanceapp.views import logOut
import datetime

class Command(BaseCommand):
    help = 'auto logout check, should be run every minute by a cron job'

    def handle(self, *args, **options):
		now = datetime.datetime.now()
		print "lol"
		if now.strftime("%A") == "Monday":
			print LabHours.objects.get(day="Monday"	).hours
			if now.time() >= LabHours.objects.get(day="Monday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
		elif now.strftime("%A") == "Tuesday":
			if now.time() >= LabHours.objects.get(day="Tuesday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
		elif now.strftime("%A") == "Wednesday":
			if now.time() >= LabHours.objects.get(day="Wednesday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
		elif now.strftime("%A") == "Thursday":
			if now.time() >= LabHours.objects.get(day="Thursday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
		elif now.strftime("%A") == "Friday":
			if now.time() >= LabHours.objects.get(day="Friday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
		elif now.strftime("%A") == "Saturday":
			if now.time() >= LabHours.objects.get(day="Saturday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
		elif now.strftime("%A") == "Sunday":
			if now.time() >= LabHours.objects.get(day="Sunday").hours:
				Students = Student.objects.filter(atLab=True)
				for student in Students: logOut(student)
