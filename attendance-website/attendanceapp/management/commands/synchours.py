from django.core.management.base import BaseCommand, CommandError
from pytz import timezone
from attendanceapp.models import LabHours, OverallStats
from datetime import datetime, timedelta, date, time
from attendanceapp.util import utc_to_normal
import urllib2
import csv
import re

class Command(BaseCommand):
    help = 'updates the lab hours from google sheet'
    def handle(self, *args, **options):
        
        print "Syncing hours with spreadsheet..."
    
    	response = urllib2.urlopen("https://docs.google.com/spreadsheets/d/e/2PACX-1vQS83DMkhEnoiz8EmjVyP40DV-HbUkZkKiGZbjKZKvlIC6cdBlYOJJcb6NfS2LuXHnZz_OT0EsxhevW/pub?gid=1449894080&single=true&output=csv")
    	data = csv.DictReader(response)
    	data = [x for x in data if datetime.strptime(x['Date'], "%m/%d/%Y") >= datetime.combine(date.today(), datetime.min.time())-timedelta(4)]
    	
    	
    	for i in data:
    		print i
    		
    	for x in data:
    	
    		starttime = datetime.combine(datetime.strptime(x['Date'], "%m/%d/%Y").date(), datetime.strptime(x['Start Time'], "%I:%M %p").time())
    		endtime = datetime.combine(datetime.strptime(x['Date'], "%m/%d/%Y").date(), datetime.strptime(x['End Time'], "%I:%M %p").time())
    		name = x['Date'] + ": " + x['Start Time'] + " - " + x['End Time']
			 		
    		hours = LabHours.objects.all().filter(starttime__gt=datetime.strptime(x['Date'], "%m/%d/%Y"), starttime__lt=datetime.strptime(x['Date'], "%m/%d/%Y")+timedelta(days=1))
    		
    		if not hours:
    			LabHours.objects.create(name=name, starttime=starttime, endtime=endtime)
    		elif len(hours) == 1:
    			if (hours[0].starttime != starttime or hours[0].endtime != endtime):
    				hours[0].starttime = starttime
    				hours[0].endtime = endtime
    				hours[0].name = name
    				hours[0].save()
    				
    		else:
    			hours.delete()
    			LabHours.objects.create(name=name, starttime=starttime, endtime=endtime)
    			
    		#does not update total time for lab hours
    		
    	print "Sync completed"
