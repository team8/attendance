from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Subteam, Student
import csv
import json
import re
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'adds slack IDs from csv file'
    def handle(self, *args, **options):
        """
        data = json.load(open(os.path.join(settings.BASE_DIR, "users.json")))

        a = []

        for x in data['members']:
            a.append((x['profile']['real_name_normalized'], x['id']))
        
        for x in a:
        
            print x
            
            students = Student.objects.all().filter(name=x[0]).first()
            
            if students:
                students.slackID = x[1]
                students.save()
        """
        """
        students = Student.objects.filter(slackID="None")
        for x in students:
            print x.name + ", " + x.slackID
        """
        file = open("data2.csv", "w")
        students = Student.objects.all()
        for x in students:
            file.write(x.name + "," + str(x.studentID) + "," + x.subteam.name + "," + x.slackID + "\n")
        file.close()
        