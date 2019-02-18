import requests
import json
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
                return "Enter a name everyone will see 'name:<username>'"


def register_name(phone, name):
    print(requests.get(CORE_API + phone + "/first/" + name))
    return True


def addPost(phone, body):
    print(CORE_API + phone + "/post/" + body)
    requests.get(CORE_API + phone + "/post/" + body)


def addDisaster(phone, state):
    r = json.loads(requests.get(CORE_API + 'disasters').text)
    disaster_areas = {}
    for pk, obj in enumerate(r):
        disaster_areas[obj['fields']['state']] = pk + 1

    if(state.upper() in disaster_areas.keys()):
        requests.get(CORE_API + phone + '/post/disaster/' +
                     str(disaster_areas[state.upper()]))


def notifyVerify(r):
    fields = json.loads(r)[0]['fields']
    msg = "Please image verify by texting us an image of your purchase and 'verify'"
    send_msg(fields['username'], msg)


@app.route('/notifyuser', methods=['GET', 'POST'])
def notifyUser():
    req = request.form.to_dict(flat=False)
    # print('REQ: ', req)
    # print(req['category'])
    msg = "You've been donated: $" + \
        req['amount'][0] + " for: " + req['category'][0] + \
        " pay with pin: " + str(req['pin'][0])
    send_msg(req['phone'][0], msg)
    return 'okay'


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Respond to incoming with a simple text message."""

    resp = MessagingResponse()
    # lower case everything and remove whitespace
    orig_body = request.values.get('Body', None)
    body = "".join(request.values.get('Body', None).lower().split())
    phonenum = request.values.get('From', None)[2:]
    from_state = request.values.get('FromState', None)
    print(body[:6])

    if(body == "helpme"):
        r = requests.get(CORE_API+phonenum).text
        msg = register_usr(phonenum, r)
        resp.message(msg)

    elif(body[:4] == 'name'):
        msg = "Okay, " + body[5:] + \
            ", text us 'newpost: <what you need (not how much)>'"
        register_name(phonenum, body[5:])
        resp.message(msg)

    elif(body[:7] == "newpost"):
        texts = orig_body.split(':')
        addPost(phonenum, texts[1])
        msg = "okay, I got your post, how much $ do you need? text us 'amount: <number>'"
        addDisaster(phonenum, from_state)
        resp.message(msg)

    elif(body[:6] == "amount"):
        amt = "".join(body[7:].split())
        requests.get(CORE_API + phonenum + "/post/amount/" + amt)
        resp.message(
            "Thanks! What category does this fall under? text 'for:<food, bottled_water>'")

    elif(body[:3] == "for"):
        print(CORE_API + phonenum + "/post/cat/" + body[4:])
        requests.get(CORE_API + phonenum + "/post/cat/" + body[4:])
        msg = "You're all set! We'll message you when someone donates!"
        resp.message(msg)

    elif(body[:7] == "payment"):
        pin = body.split(":")[1]
        r = requests.get(CORE_API + phonenum + "/transaction/" + pin).text
        notifyVerify(r)
        msg = "You just got paid! Check your account"
        resp.message(msg)

    elif(body[:6] == "verify"):
        if request.values['NumMedia'] != '0':
            image_url = request.values['MediaUrl0']
            msg = requests.get(image_url).content
            pred = cv_verify.predict(msg, PROJECT_ID, MODEL_ID)

            label = pred.payload[0].display_name

            requests.get(CORE_API + phonenum + "/user/" + label)
            msg = "You verified with a picture of " + label
            resp.message(msg)
        else:
            resp.message("You need to verify with a picture!")

    else:
        resp.message("Emergency? Make a request by sending 'help me'")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
