from django.conf import settings
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN
SLACK_BOT_TOKEN = settings.SLACK_BOT_TOKEN

import logging
logging.getLogger().setLevel(logging.INFO)

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
    
    print message["bot_id"]
    print message["bot_id"] is None
    print message["bot_id"] == ""
    
    if message.get("subtype") is None:
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        message += "\nI will tell you if you've forgotten to log out of the attendance system."
        logging.info("chat.postMessage: channel: %s text: %s" % (channel, message))
        CLIENT.api_call("chat.postMessage", channel=channel, text=message, as_user=True)