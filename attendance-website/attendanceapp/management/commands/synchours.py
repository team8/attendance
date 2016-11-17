from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from attendanceapp.models import LabHours
from datetime import datetime
import urllib

class Command(BaseCommand):
	help = 'updates the lab hours weekly'
	def handle(self, *args, **options):
		LabHours.objects.all().delete()
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
		events = CAL.events().list(calendarId="db25n7oev1at726gljle5d784c@group.calendar.google.com", singleEvents = True, timeMin = datetime_phrase).execute()
		for event in events['items']:
			if event['summary'].startswith("LAB OPEN"):
				print (event['summary'] + " " + event['end'].get("dateTime"))
				LabHours.objects.create(name=event['summary'], starttime = event['start'].get("dateTime"), endtime=event['end'].get("dateTime"))