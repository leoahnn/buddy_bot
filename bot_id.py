import os
from slackclient import SlackClient


BOT_NAME = 'buddy_bot'

sc = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def get_id():
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')
    else:
        print ("api call not okay")
