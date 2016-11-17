from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Student, HoursWorked
from attendanceapp.views import logOut

class Command(BaseCommand):
    help = 'clears all hours and logs everyone out'
	
    def handle(self, *args, **options):
        HoursWorked.objects.all().delete()
        for person in Student.objects.all():
            print "another one"
            if person.atLab:
                logOut(person, False, False, False)
            person.totalTime = 0
            person.hoursWorked.through.objects.all().delete()
            person.save()