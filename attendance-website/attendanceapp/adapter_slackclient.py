from django.conf import settings
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN
SLACK_BOT_TOKEN = settings.SLACK_BOT_TOKEN

import logging
logging.getLogger().setLevel(logging.INFO)

from attendanceapp.models import Student

from pyee import EventEmitter
from slackclient import SlackClient
CLIENT = SlackClient(SLACK_BOT_TOKEN)

from datetime import datetime, timedelta, date, time


class SlackEventAdapter(EventEmitter):
    def __init__(self, verification_token):
        EventEmitter.__init__(self)
        self.verification_token = verification_token

slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN)


# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message

    if message.get("subtype") is None and message.get('bot_id') == None:
        channel = message["channel"]
        msg = message.get('text').lower()
        if "thanks" in msg or "thank you" in msg:
            text = "No problem!  Just doing my job :smile:"
        elif "hi" in msg or "hello" in msg or "hey" in msg:
            text = "Hello <@%s>! :tada:" % message["user"]
        elif ("in" in msg or "at" in msg) and "lab" in msg:
            students = Student.objects.filter(atLab = True)
            if not students:
                text = "There is no one currently at the lab."
            else:
                text = "The following people are currently at the lab:  "
                for i in students:
                    text = text + i.name + ", "
                text = text.rstrip(", ")
        elif "hour" in msg:
            student = Student.objects.filter(slackID = message["user"]).first()
            if student != None:
                if "log" in msg:
                    text = "Here is a detailed output of your logged hours:\n"
                    hours = student.hoursWorked.all()
                    output = sorted([(h.timeIn, h.timeOut) for h in hours], key=lambda x: x[0], reverse=True)
                    for i in output:
                        text+=i[0].strftime("%m/%d/%y") + ": " + i[0].strftime("%I:%M %p") + " - " + i[1].strftime("%I:%M %p") + "\n"
                    text = text.strip()
                    if text[-1] == ":":
                        text = "You have not logged any hours in the attendance system yet."
                else:
                    text = "You have currently logged " + str(round(student.totalTime/3600.0, 2)) + " hours in total and "  + str(round(student.validTime/3600.0, 2)) + " hours during official lab hours this season."
            else:
                text = "Sorry, you don't seem to be registered in the attendance system!"
        else:
            text = "Greetings <@%s>! :tada:" % message["user"]
            text += "\nI will tell you if you've forgotten to log out of the attendance system."
            text += "\nYou can ask me who is at the lab."
            text += "\nI can also tell you how many hours you have logged this season."
        logging.info("chat.postMessage: channel: %s text: %s" % (channel, text))
        CLIENT.api_call("chat.postMessage", channel=channel, text=text, as_user=True)