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
        
        message = "Hello! Outstanding requested lab hour changes:\n\n"
                
        if not HoursWorkedEditSet.objects.all().exists():
            message += "*No outstanding requests*\n"
        else:
            for s in HoursWorkedEditSet.objects.all():
                message += self.setToString(s) + "\n"
        
        message += "\nType `approve` to approve all outstanding changes, or `deny <id> [reason]` to deny specifc changes. Type `changes` to display a refreshed list of requested changes."
        
        dm_id = CLIENT.api_call("im.open", user=options["user"], return_im=True)['channel']['id']
        CLIENT.api_call("chat.postMessage", channel=dm_id, text=message, as_user=True)
    
    @staticmethod
    def setToString(a):
        s = []
        t = []
        for x in a.contents.all():
            timeIn = x.newTimeIn or x.timeIn
            timeOut = x.newTimeOut or x.timeOut
            if abs((timeIn-timeOut).total_seconds()) > 2:
                s.append((timeIn, timeOut))
            if abs((x.timeIn-x.timeOut).total_seconds()) > 2:
                t.append((x.timeIn, x.timeOut))
        s = sorted(s, key=lambda y: y[0])
        t = sorted(t, key=lambda y: y[0])
        
        message =  "*(" +  str(a.pk) + ")* " + a.owner.name + "\n>(" + a.date.strftime("%m/%d/%y") + ")"
        if t:
            message += "\n>*Original*\n>" + "\n>".join(i[0].strftime("%I:%M %p") + " - " + i[1].strftime("%I:%M %p") for i in t)
        else:
            message += "\n>*Original*\n>No hours"
        if s:
            message += "\n>*Modified*\n>" + "\n>".join(i[0].strftime("%I:%M %p") + " - " + i[1].strftime("%I:%M %p") for i in s)
        else:
            message += "\n>*Modified*\n>No hours"
        return message
        
        
        
