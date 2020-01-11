from attendanceapp.adapter_slackclient import CLIENT
from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import Student, HoursWorked

import csv
import re
import os
from django.conf import settings

from datetime import datetime, timedelta, date, time

class Command(BaseCommand):

    def handle(self, *args, **options):
    	
        file = open(os.path.join(settings.BASE_DIR, "hours.csv"))
        data = list(csv.DictReader(file))
        

        for x in data:
        	studentID = x["studentID"]
        	student = Student.objects.filter(studentID=studentID).first()
        	if not student:
        		continue
        	timeIn = datetime.strptime(x["timeIn"], "%d/%m/%Y %H:%M:%S")
        	timeOut = datetime.strptime(x["timeOut"], "%d/%m/%Y %H:%M:%S")
        	        	
        	h = HoursWorked(owner=student, timeIn=timeIn, timeOut=timeOut)
        	h.save()
        	
        	student.hoursWorked.add(h);
        	student.save();
        
        """
        students = Student.objects.all()
        for s in students:
        	dates = list(set([x.timeIn.date() for x in s.hoursWorked.all()]))
        	for x in dates:
        		hrs = s.hoursWorked.filter(timeIn__gt=datetime.combine(x, datetime.min.time()), timeIn__lt=datetime.combine(x, datetime.min.time())+timedelta(days=1))
        		if len(hrs) > 1:
        			dm_id = CLIENT.api_call("im.open", user=s.slackID, return_im=True)['channel']['id']
        			message = "Hi " + s.name.split(" ")[0] + "--you have multiple lab hour entries on " + str(x) + ". Please check your hours using `hours log` and submit any neccesary attendance changes at attendance.palyrobotics.com:8000/fixHours/"
        			CLIENT.api_call("chat.postMessage", channel=dm_id, text=message, as_user=True)
        """