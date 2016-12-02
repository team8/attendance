from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Student, HoursWorked, Subteam
from attendanceapp.views import logOut

class Command(BaseCommand):
    help = 'clears all hours and logs everyone out'
	
    def handle(self, *args, **options):
        for person in Student.objects.all():
            if person.atLab:
                logOut(person, False, False, False)
            person.totalTime = 0
            person.averageTime = 0
            person.stddevTime = 0
            person.daysWorked = 0
            person.percentDaysWorked = 0
            person.averagePercentTimeWeighted = 0
            person.stddevPercentTimeWeighted = 0
            person.mostFrequentDay = "None"
            person.hoursWorked.through.objects.all().delete()
            person.save()
            
        for subteam in Subteam.objects.all():
            subteam.averagePercentTimeWeighted = 0
            subteam.stddevPercentTimeWeighted = 0
            subteam.mostFrequentDay = 0
            subteam.totalDaysWorked = 0
            subteam.save()
        HoursWorked.objects.all().delete()