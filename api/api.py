from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("Sup bitch")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

""" gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="user:cjl.roncal@gmail.com" \
   --role="roles/automl.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:aidapi" \
   --role="roles/automl.editor"

gsc """