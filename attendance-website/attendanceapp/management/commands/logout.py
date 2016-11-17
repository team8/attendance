from django.core.management.base import BaseCommand, CommandError
from attendanceapp.models import LabHours, Student
from attendanceapp.views import logOut
from datetime import datetime, timedelta
import calendar

class Command(BaseCommand):

    help = 'updates lab hours model, should be run every week by a cron job'
	
    def handle(self, *args, **options):
	
		#hehe ecks dee deal with google calendar utc format
		utctime = LabHours.objects.order_by("endtime").first().endtime
		timestamp = calendar.timegm(utctime.timetuple())
		local_dt = datetime.fromtimestamp(timestamp)
		assert utctime.resolution >= timedelta(microseconds=1)
		realhours = local_dt.replace(microsecond=utctime.microsecond)
		
		now = datetime.now()
        
		if (realhours + timedelta(hours=2)) < now:
			everyone = Student.objects.filter(atLab = True)
			for student in everyone:
				logOut(student, False, True, True)
			LabHours.objects.order_by("endtime").first().delete()