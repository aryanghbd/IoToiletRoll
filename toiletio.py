import os
import time
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import smbus2
from time import sleep
from twilio.rest import Client

import paho.mqtt.client as mqtt
import json
import tweepy
import random
import requests

from threading import Timer
import threading
import urllib
import subprocess

from sms import *
from mqtt import *
from meme_utils import *
from utils import *


app = Flask(__name__)



mqtt_client = mqtt.Client()
mqtt_client.connect("test.mosquitto.org", port=1883)
mqtt_client.subscribe("IC.embedded/Useless_System")
mqtt_client.subscribe("IC.embedded/Useless_System/Household")
mqtt_client.on_message = on_message
mqtt_client.loop_start()

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    global test_string
    test_string = body
    # Start our TwiML response
    resp = MessagingResponse()
    global meme_flag
    # Determine the right reply for this message
    if body == 'MEME':
        meme_flag = True
        resp.message("Time to start rolling, " + get_current_user() + ", we'll handle the memes.")
    elif body == 'NO MEME':
        meme_flag = False
        resp.message("Response acknowledged, you may now roll")
    else:
        dispatch_text(number="+447711223376", content="test")

    return str(resp)

@app.route("/")
def main():
    if not os.path.isfile('household.json'):
        print("Waiting for file")
        while not check_for_household():
            pass
    else:
        with open('household.json') as file:
            global household
            household = json.load(file)
        print("Welcome users")
        print(household)


    while True:
        print("Now waiting for next user...")
        while not start_flag:
            pass
        name = get_current_user()
        number = get_number()
        print("Hello user: " + name)
        print(start_flag)
        print(meme_flag)
        print(test_string)
        dispatch_text(number, "Welcome user: " + name + " Would you be interested in a meme after your session finishes?")
        while meme_flag is None:
            pass
        bus = initialize()
        measure(bus, name, number, mqtt_client)

        #test

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0') #Test