import json
from twilio.rest import Client

account_sid = 'AC41b90ac7261fcc6918eb596424aeae2c'
auth_token = 'b616627909a0035c96a67d6a5934505e'
from_num = '+12024706272'

def send_msg(number, msg):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                              from_=from_num,
                              body=msg,
                              to=number
                          )

def get_fields(r):
    return json.loads(r)[0]['fields']