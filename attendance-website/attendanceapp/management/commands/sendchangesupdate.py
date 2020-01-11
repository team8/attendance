from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student, HoursWorked, HoursWorkedEditSet
from django.core.management import call_command

class Command(BaseCommand):

    help = 'automatically logs out students'
    
    def handle(self, *args, **options):
        
        admins = Student.objects.filter(admin=True)
        
        for x in admins:
			call_command('approve', user=x.slackID)