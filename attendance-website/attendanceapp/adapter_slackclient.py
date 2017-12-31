from django.conf import settings
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN
SLACK_BOT_TOKEN = settings.SLACK_BOT_TOKEN

import logging
logging.getLogger().setLevel(logging.INFO)

from attendanceapp.models import Student

from pyee import EventEmitter
from slackclient import SlackClient
CLIENT = SlackClient(SLACK_BOT_TOKEN)


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
            if students == None:
                text = "There is no one currently at the lab."
            else:
                text = "The following people are currently at the lab:  "
                for i in students:
                    text = text + i.name + ", "
                text = text.rstrip(", ")
        else:
            text = "Greetings <@%s>! :tada:" % message["user"]
            text += "\nI will tell you if you've forgotten to log out of the attendance system."
            text += "\nYou can also ask me who is at the lab."
        logging.info("chat.postMessage: channel: %s text: %s" % (channel, text))
        CLIENT.api_call("chat.postMessage", channel=channel, text=text, as_user=True)