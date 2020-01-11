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
        print "Auto logout starting..."
        for person in Student.objects.all():
            sentMessage = False
            if person.atLab:
                logOut(person)
                dm_id = CLIENT.api_call("im.open", user=person.slackID, return_im=True)['channel']['id']
                message = "Hi " + person.name.split(" ")[0] + "--you forgot to log in or log out at the lab yesterday (" + (date.today()-timedelta(days=1)).strftime("%m/%d/%y") + ").  Please submit attendance changes at attendance.palyrobotics.com:8000/fixHours/ and feel free to contact @<U2S7Z0UCD> with any questions."
                CLIENT.api_call("chat.postMessage", channel=dm_id, text=message, as_user=True)
                sentMessage=True
            """
            autoLogoutHours = person.hoursWorked.filter(autoLogout=True) & person.hoursWorked.filter(totalTime__lt = 60.0)
            
            if autoLogoutHours:
                dm_id = CLIENT.api_call("im.open", user=person.slackID, return_im=True)['channel']['id']
                dates = set()
                for h in autoLogoutHours:
                    dates.add(h.timeIn.date())
                dates = sorted(dates)
                if sentMessage:
                    message = "Furthermore, a reminder that your lab attendance entries for the following dates also need to be corrected:\n"
                    for d in dates:
                        if d != date.today()-timedelta(days=1):
                            message += d.strftime("%m/%d/%y") + "\n"
                    message = message.strip()
                    if message[-1] == ":":
                        continue
                else:
                    message = "Hi " + person.name.split(" ")[0] + "--a reminder that your lab attendance entries for the following dates need to be corrected by contacting <@U039ZJW8K> and providing the time you arrived and left:\n"
                    for d in dates:
                        message += d.strftime("%m/%d/%y") + "\n"
                    message = message.strip()
                
                CLIENT.api_call("chat.postMessage", channel=dm_id, text=message, as_user=True)
                #print message
            """ 
        print "Auto logout completed"
                
                
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