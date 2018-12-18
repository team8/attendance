from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student, HoursWorked, HoursWorkedEditSet
from attendanceapp.adapter_slackclient import CLIENT

from datetime import datetime, timedelta, date
from pytz import timezone
from attendanceapp.util import do_student_calcs
import pytz
import calendar
import hashlib

class Command(BaseCommand):

    help = 'automatically logs out students'
    
    def handle(self, *args, **options):
    
        message = "Hello!  Daily Approval Update:\n\n"
    
        for s in HoursWorkedEditSet.objects.all():
            message += self.setToString(s) + "\n"
        
        message += "\nType `approve` to approve all of these changes, or `deny <id> <reason>` to deny specifc changes."
            
        print message
    
    @staticmethod
    def setToString(a):
        s = []
        for x in a.contents.all():
            timeIn = x.newTimeIn or x.timeIn
            timeOut = x.newTimeOut or x.timeOut
            #if (timeIn-timeOut).total_seconds() > 1:
            s.append((timeIn, timeOut))
        s = sorted(s, key=lambda y: y[0])
        
        return "*(" +  str(a.pk) + ")* " + a.owner.name + "\n>(" + a.date.strftime("%m/%d/%y") + ")\n>" + "\n>".join(i[0].strftime("%I:%M %p") + " - " + i[1].strftime("%I:%M %p") for i in s)
        
        