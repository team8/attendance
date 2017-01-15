from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student, HoursWorked, OverallStats
from attendanceapp.views import logOut
from datetime import datetime, timedelta
from pytz import timezone
from attendanceapp.util import do_student_calcs
import pytz
import calendar

class Command(BaseCommand):

    help = 'automatically logs out students'
    def handle(self, *args, **options):
        try:    
            labtime = LabHours.objects.filter(used = False).order_by("starttime").first().endtime
            timestamp = calendar.timegm(labtime.timetuple())
            local_dt = datetime.fromtimestamp(timestamp)
            assert labtime.resolution >= timedelta(microseconds=1)
            realhours = local_dt.replace(microsecond=labtime.microsecond)
            realhours = realhours.replace(tzinfo = (timezone('US/Pacific')))
        except:
            labtime = pytz.utc.localize(datetime.strptime('Jan 1 2020  12:00AM', '%b %d %Y %I:%M%p'))
        now = datetime.now(tz=pytz.utc)
        now = now.astimezone(timezone('US/Pacific'))
        oldtime = pytz.utc.localize(datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p'))
        
        for person in Student.objects.all():
            if (person.lastLoggedIn.date() != now.date()) and (not person.atLab):    #change this after build season   
                worthlessHours = HoursWorked(timeIn=oldtime,day = "None",timeOut=oldtime, totalTime=0.0, autoLogout=True, outsideLabHours = True, weight = LabHours.objects.filter(used = False).order_by("endtime").first().totalTime)
                worthlessHours.save()
                person.hoursWorked.add(worthlessHours)
                person.save()
            if person.atLab:
                logOut(person, False, True, True)
            do_student_calcs(person)
        if labtime < now:   
            first = LabHours.objects.filter(used=False).order_by("endtime").first()
            first.used = True
            first.save()
           
        totalhours = 0
        totaldays = 0
        for hours in LabHours.objects.all():
            totalhours += hours.totalTime
            totaldays += 1
        overall = OverallStats.objects.get(name="Overall Stats")
        overall.totalLabHours = totalhours
        overall.totalLabDays = totaldays
        overall.save()