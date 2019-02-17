import requests, json
import cv_verify
from util import get_fields
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
PROJECT_ID = 'glossy-motif-231903'
MODEL_ID = 'ICN8597385071115107724'
CORE_API = 'http://22b17c96.ngrok.io/api/'

signup_order = ['first_name']


def register_usr(phone, r):
  fields = get_fields(r)

  for field in signup_order:
    if fields[field] == "":
      if field == 'first_name':
        return "Enter a name everyone will see"

def ensure_name(phone, r, name):
  fields = get_fields(r)
  
  if fields['first_name'] == '':
    requests.post(CORE_API + phone + "/first/" + name)
    return True
  return False

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Respond to incoming with a simple text message."""

    resp = MessagingResponse()
    #lower case everything and remove whitespace
    body = "".join(request.values.get('Body', None).lower().split())
    phonenum = request.values.get('From', None)[2:]
    from_state = request.values.get('FromState', None)
    from_country = request.values.get('FromCountry', None)

    if(body == "helpme"):
      r = requests.get(CORE_API+phonenum).text
      msg = register_usr(phonenum, r)
      resp.message(msg)

    else:
      if ensure_name(phonenum, r, body):
        resp.message("Okay, ", body, "request for donations by texting 'mypost: <your request here>'")
      else:
        resp.message("Emergency? Make a request by sending 'help me'")

    # if request.values['NumMedia'] != '0':

    #     # Use the message SID as a filename.
    #     image_url = request.values['MediaUrl0']
    #     msg = requests.get(image_url).content
    #     pred = cv_verify.predict(msg, PROJECT_ID, MODEL_ID) 

    #     print(pred.payload[0])
    #     resp.message(pred.payload[0].display_name)
    # else:
    #     resp.message("Try sending a picture message.")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)