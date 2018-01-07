from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student, HoursWorked, OverallStats
from attendanceapp.adapter_slackclient import CLIENT

from datetime import datetime, timedelta, date
from pytz import timezone
from attendanceapp.util import do_student_calcs
import pytz
import calendar

class Command(BaseCommand):

    help = 'automatically logs out students'
    
    def handle(self, *args, **options):
        for person in Student.objects.all():
            if person.atLab:
                logOut(person)
                dm_id = CLIENT.api_call("im.open", user=person.slackID, return_im=True)['channel']['id']
                message = "Hi " + person.name.split(" ")[0] + "--you forgot to log out before leaving the lab yesterday (" + (date.today()-timedelta(days=1)).strftime("%m/%d/%y") + ").  Please contact <@U039ZJW8K> with the time you left the lab in order to have the entry in the attendance system corrected."
                CLIENT.api_call("chat.postMessage", channel=dm_id, text=message, as_user=True)
                
def logOut(student):
    #Tell the system that the student is no longer in the lab
    student.atLab=False
    
    #load the last logged in time into memory
    timeIn=student.lastLoggedIn
    
    timeWorked=HoursWorked(timeIn=timeIn,timeOut=timeIn,owner=student,autoLogout=True)
    timeWorked.save()
    #add the time worked object to the student so it can be viewed in the calander
    student.hoursWorked.add(timeWorked)
    #add the minutes to the student's total time
    student.save()