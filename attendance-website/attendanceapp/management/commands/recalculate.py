from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Student, HoursWorked, Subteam
from attendanceapp.views import logOut
import datetime

class Command(BaseCommand):
    help = 'recalculates student stats'
	
    def handle(self, *args, **options):
        for person in Student.objects.all():
            person.save()
        for subteam in Subteam.objects.all():
            subteam.save()