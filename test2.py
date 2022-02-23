from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import utils

app = Flask(__name__)
account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
client = Client(account_sid, auth_token)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'YES':
        resp.message("Meme generated")
        utils.generate_meme(utils.current_msg, utils.current_sheets)
    elif body == 'NO':
        resp.message(":D")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=False)