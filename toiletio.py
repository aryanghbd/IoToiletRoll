from flask import Flask, request, redirect

from twilio.twiml.messaging_response import MessagingResponse
import utils
app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'YES':
        resp.message("Meme generated, check out Twitter!")
    elif body == 'NO':
        resp.message("No meme generated")

    return str(resp)

@app.route('/')
def runroll():
    file = open('utils.py', 'r').read()
    return exec(file)

if __name__ == "__main__":
    app.run(debug=False)