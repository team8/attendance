from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Subteam, Student
import csv
import re
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'adds students from csv file'
    def handle(self, *args, **options):
    
        file = open(os.path.join(settings.BASE_DIR, "data2.csv"))
        data = list(csv.DictReader(file))
        
        subteams = []
        for x in data:
            if x['Subteam'] not in subteams:
                subteams.append(x['Subteam'])   
        for x in subteams:
            existing_subteams = Subteam.objects.all().filter(name=x).first()
            if not existing_subteams:
                Subteam.objects.create(name=x)
        
        for x in data:
            students = Student.objects.all().filter(studentID=x['ID#']).first()
            if not students:
                Student.objects.create(name=x['Full Name'], studentID=x['ID#'], subteam=Subteam.objects.get(name=x['Subteam']), slackID=x['Slack ID'])
            else:
                students.slackID = x['Slack ID']
                students.save()