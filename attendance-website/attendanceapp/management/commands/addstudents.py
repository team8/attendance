from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Subteam, Student
import csv
import re
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'adds students from csv file'
    def handle(self, *args, **options):
    
        file = open(os.path.join(settings.BASE_DIR, "data.csv"))
        data = list(csv.DictReader(file))
        subteams = []
        for x in data:
            if x['Subteam'] not in subteams:
                subteams.append(x['Subteam'])   
        for x in subteams:
            s = Subteam(name=x)
            s.save();
        
        for x in data:
            s = Student(name=x['Full Name'], studentID=x['ID#'], subteam=Subteam.objects.get(name=x['Subteam']), slackID=x['Slack ID'])
            s.save();