import json
from twilio.rest import Client

account_sid = '#'
auth_token = '#'
from_num = '#'


def send_msg(number, msg):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_num,
        body=msg,
        to=number
    )


def get_fields(r):
    return json.loads(r)[0]['fields']
