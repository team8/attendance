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
        text = ""
        if message["user"] == "U039ZJW8K":
            text = handleAdminCommands(msg, message["user"])
        if not text:
            text = handleNormalCommands(msg, message["user"])
        
        logging.info("chat.postMessage: channel: %s text: %s" % (channel, text))
        CLIENT.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

def handleAdminCommands(message, user):
    text = ""
    if "approve" in message:
        text = "Great!  All changes have been approved."
    elif "deny" in message:
        splitMsg = message.split(" ", 2)
        id = int(splitMsg[1])
        msgToMember = splitMsg[2].strip()
        text = "Change *" + str(id) +"* has been denied. A notifcation has been sent to the student."
    return text

def handleNormalCommands(message, user):
    text = ""
    if "thanks" in message or "thank you" in message:
        text = "No problem!  Just doing my job :smile:"
    elif "hi" in message or "hello" in message or "hey" in message:
        text = "Hello <@%s>! :tada:" % user
    elif "hi" in message:
        if "eraine" in message:
            text = "Hello <@%s>! :tada:" % user
    elif ("in" in message or "at" in message) and "lab" in message:
        students = Student.objects.filter(atLab = True)
        if not students:
            text = "There is no one currently at the lab."
        else:
            text = "The following people are currently at the lab:  "
            for i in students:
                text = text + i.name + ", "
            text = text.rstrip(", ")
    elif "hour" in message:
        student = Student.objects.filter(slackID = user).first()
        if student != None:
            if "log" in message:
                text = "Here is a detailed output of your logged hours:\n"
                hours = student.hoursWorked.all()
                output = sorted([(h.timeIn, h.timeOut) for h in hours], key=lambda x: x[0], reverse=True)
                for i in output:
                    text+=i[0].strftime("%m/%d/%y") + ": " + i[0].strftime("%I:%M %p") + " - " + i[1].strftime("%I:%M %p") + "\n"
                text = text.strip()
                if text[-1] == ":":
                    text = "You have not logged any hours in the attendance system yet."
            elif "build" in message:
                total = 0
                valid_total = 0
                for i in student.hoursWorked.filter(timeIn__gte=datetime(2018, 1, 6), timeIn__lt=datetime(2018, 2, 21)):
                    total += i.totalTime
                    valid_total += i.validTime
                text = "You logged " + str(round(total/3600.0, 2)) + " hours in total during build season and "  + str(round(valid_total/3600.0, 2)) + " hours during official lab hours."
            else:
                text = "You have currently logged " + str(round(student.totalTime/3600.0, 2)) + " hours in total and "  + str(round(student.validTime/3600.0, 2)) + " hours during official lab hours this season."
        else:
            text = "Sorry, you don't seem to be registered in the attendance system!"
    else:
        text = "Greetings <@%s>! :tada:" % user
        text += "\nI will tell you if you've forgotten to log out of the attendance system."
        text += "\nYou can ask me who is at the lab."
        text += "\nI can also tell you how many hours you have logged this season."
        
    return text