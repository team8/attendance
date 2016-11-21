from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student, HoursWorked
from attendanceapp.views import logOut
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
#change this to run once a day at like 11:55pm or something since autologout does not save hours
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
        if realhours < now:
            for person in Student.objects.all():
                if person.lastLoggedIn.date() != now.date():
                    worthlessHours = HoursWorked(timeIn=now,day = now.strftime("%A"),timeOut=now, totalTime=0.0, autoLogout=True, outsideLabHours = True, weight = 0.0)
                    worthlessHours.save()
                    person.hoursWorked.add(worthlessHours)
                elif person.atLab:
                    logOut(person, False, True, True)
            first = LabHours.objects.filter(used=False).order_by("endtime").first()
            first.used = True
            first.save()