from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from attendanceapp.models import LabHours, OverallStats
from datetime import datetime, timedelta
from attendanceapp.util import utc_to_normal
import urllib
import re

class Command(BaseCommand):
    help = 'updates the lab hours weekly'
    def handle(self, *args, **options):
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('/home/bdavies/.credentials/calendar-python-quickstart.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store, flags) \
                    if flags else tools.run(flow, store)
        CAL = build('calendar', 'v3', http=creds.authorize(Http()))
        datetime_phrase = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') #i honestly hate time formats jeez
        datetime_phrase += 'Z'
        week_from_now = (datetime.utcnow() + timedelta(days = 7)).strftime('%Y-%m-%dT%H:%M:%S')
        week_from_now += 'Z'
        events = CAL.events().list(calendarId="db25n7oev1at726gljle5d784c@group.calendar.google.com", singleEvents = True, timeMin = datetime_phrase, timeMax = week_from_now).execute()
        for event in events['items']:
            if event['summary'].startswith("LAB OPEN"):
                LabHours.objects.create(name=event['summary'], starttime = event['start'].get("dateTime"), endtime=event['end'].get("dateTime")+timedelta(hours=1), totalTime = getTimeDiff(event))
def getTimeDiff(event):
    a = event['start'].get('dateTime').replace(' ', '')[:-6]
    b = event['end'].get('dateTime').replace(' ', '')[:-6]
    aobj = datetime.strptime(a, '%Y-%m-%dT%H:%M:%S')
    bobj = datetime.strptime(b, '%Y-%m-%dT%H:%M:%S')
    c = bobj-aobj
    minutes, seconds = divmod(c.total_seconds(), 60)
    hours, minutes = divmod(minutes, 60)
    minutesdecimal = minutes/60
    result = hours+minutesdecimal+1
    return result