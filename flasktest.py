import flask
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    flask.render_template("serverresponse.html")
    while True:
        print("what's up")
    return 0
@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    #Test
    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'YES':
        resp.message("Meme generated")
    elif body == 'NO':
        resp.message(":D")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')