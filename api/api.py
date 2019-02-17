import requests, json
import cv_verify
from util import get_fields, send_msg
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

def ensure_name(phone, name):
  r = requests.get(CORE_API+phone).text
  fields = get_fields(r)
  if fields['first_name'] == '':
    print(requests.get(CORE_API + phone + "/first/" + name))
    return True
  return False

def addPost(phone, body):
  print(CORE_API + phone + "/post/" +body)
  requests.get(CORE_API + phone + "/post/" +body )

def addDisaster(phone, state):
  r = json.loads(requests.get(CORE_API + 'disasters').text)
  disaster_areas = {}
  for pk, obj in enumerate(r):
    disaster_areas[obj['fields']['state']] = pk + 1

  if(state.upper() in disaster_areas.keys()):
    requests.get(CORE_API + phone + '/post/disaster/' + str(disaster_areas[state.upper()]))

@app.route('/notifyuser', methods=['GET', 'POST'])
def notifyUser():
  req = request.form.to_dict(flat=False)
  msg = "You've been donated: $" + req['amount'][0] + " pin: " + req['pin'][0]
  send_msg(req['phone'][0], msg)
  

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Respond to incoming with a simple text message."""

    resp = MessagingResponse()
    #lower case everything and remove whitespace
    body = "".join(request.values.get('Body', None).lower().split())
    phonenum = request.values.get('From', None)[2:]
    from_state = request.values.get('FromState', None)
    #from_country = request.values.get('FromCountry', None)

    if(body == "helpme"):
      r = requests.get(CORE_API+phonenum).text
      msg = register_usr(phonenum, r)
      resp.message(msg)
    
    elif(body[:7] == "newpost"):
      addPost(phonenum, body[8:])
      msg = "okay, I got your post, how much do you need? text us 'amount: <number>'"
      addDisaster(phonenum, from_state) 
      resp.message(msg)

    elif(body[:6] == "amount"):
      amt = "".join(body[7:].split())
      requests.get(CORE_API + phonenum + "/post/amount/" + amt)
      resp.message("Thanks! What's this for? text 'for:<food, bottled_water>'")

    elif(body[:2] == "for"):
      requests.get(CORE_API + phonenum + "post/cat/" + body[3:])
      msg = "You're all set! We'll message you when someone donates!"
      resp.message(msg)

    else:
      if ensure_name(phonenum, body):
        msg = "Okay, " + body + ", text us 'newpost: <what you need (not how much)>'"
        resp.message(msg)
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