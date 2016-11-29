from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student, HoursWorked
from attendanceapp.views import logOut
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar

class Command(BaseCommand):

    help = 'automatically logs out students'
	
    def handle(self, *args, **options):
    
        utctime = LabHours.objects.filter(used = False).order_by("endtime").first().endtime
        timestamp = calendar.timegm(utctime.timetuple())
        local_dt = datetime.fromtimestamp(timestamp)
        assert utctime.resolution >= timedelta(microseconds=1)
        realhours = local_dt.replace(microsecond=utctime.microsecond)
        realhours = realhours.replace(tzinfo = (timezone('US/Pacific')))
        now = datetime.now(tz=pytz.utc)
        now = now.astimezone(timezone('US/Pacific'))
        oldtime = pytz.utc.localize(datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p'))
        
        for person in Student.objects.all():
            if LabHours.objects.filter(used = False).order_by("endtime").first().endtime.date() == now.date():
                if person.lastLoggedIn != now.date():     
                    worthlessHours = HoursWorked(timeIn=oldtime,day = "None",timeOut=oldtime, totalTime=0.0, autoLogout=True, outsideLabHours = True, weight = 0.0)
                    worthlessHours.save()
                    person.hoursWorked.add(worthlessHours)
                    person.save()
            if person.atLab:
                logOut(person, False, True, True)
                
        if realhours < now:   
            first = LabHours.objects.filter(used=False).order_by("endtime").first()
            first.used = True
            first.save()