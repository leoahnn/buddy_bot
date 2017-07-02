import os
import time
from slackclient import SlackClient
from bot_id import get_id

BOT_ID = get_id()
#BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"
TRAINER = "U2RLLPDK6"


sc = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel, user):
    print("command" + command)
    response = "bark!"
    if TRAINER in user:
        response = "YOU ARE THE BEST"
    if "buddy" in command:
        response = "bark bark?"
    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(rtm_output):
    output_list = rtm_output
    print output_list
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and BOT_ID in output['text']:
                print("a hit!")
                return output['text'].split(BOT_ID)[1].strip().lower(), \
                       output['channel'], output['user']
    return None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print("buddy bot is off and running!")
        print AT_BOT
        while True: 
            (command, channel, user) = parse_slack_output(sc.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("connection failed")


