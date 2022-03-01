import os
import time
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from time import sleep
from twilio.rest import Client

import paho.mqtt.client as mqtt
import json
import tweepy

import accel_i2c
import string_utils
from meme import generate_meme, generate_meme_text

from threading import Timer
import threading
import urllib
import subprocess

app = Flask(__name__)

#Global client in order to pass into functions.
username = 'toilet.io'
password = 'Toilettime'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'

tweetclient = tweepy.Client(consumer_key='NJR2pGSoieZyRk9jTPC4ypO9Z',
                       consumer_secret='L2GeDyGGzL0hezXQQJ5sF86g3nIlD7jg5DscebiSWgtd5ayC2N',
                       access_token='1496564796950519808-CNGNNX1gkZPSpqANxDUL73nFcrPkQM',
                       access_token_secret='vYFMKnfHdCFOGh8buoVtoNJ3Yw6oL9kOk7Gl09wThqiYa')


account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'

mqtt_client = mqtt.Client()
mqtt_client.connect("test.mosquitto.org", port=1883)
mqtt_client.subscribe("IC.embedded/Useless_System")
mqtt_client.subscribe("IC.embedded/Useless_System/Household")



client = Client(account_sid, auth_token)

current_msg = ''
last_user = ''
household = []
start_flag = False
meme_flag = None
roll_flag = False
test_string = ''
current_sheets = 0.0
rolls = 0.0

def dispatch_text(number, content):
    message = client.messages \
        .create(
        body=content,
        from_='+447897016821',
        to=number
    )
    return 0

def get_final_sheets():
    return current_sheets

def check_user(username):
    for person in household:
        if username == person['name']:
            return True
    return False

def get_number():
    name = get_current_user()
    for person in household:
        if name == person['name']:
            return (person['number'])

def get_current_user():
    return current_msg
#Getter function for ease of use

def reset(revolutions, axis, rolls):
    print("Sorry, resetting now!")
    revolutions = 0
    axis = None
    global current_msg, start_flag, meme_flag, current_sheets
    current_msg = ""
    start_flag = False
    meme_flag = None
    current_sheets = 0.0
    with open('rolls.txt', 'w') as file:
        file.write(str(rolls))
    return revolutions, axis

def check_for_household():
    if len(household) != 0:
        return True

def measure(bus, name, number):
    dispatch_text(number, "You may now begin rolling.")
    global rolls, last_user
    while True:
        #lastZ = None
        axis = None
        revolutions = 0
        #current_max = get_max()
        t_s = time.time()
        while True:
            X = accel_i2c.get_X(bus)
            Y = accel_i2c.get_Y(bus)
            Z = accel_i2c.get_Z(bus)
            if Z < -7.5 and axis == None:
                axis = Z
            if Z > 8 and axis != None:
                revolutions = revolutions + 1
                rolls = rolls - 1.5
                print("Rolled! Number of revolutions: " + str(revolutions))
                print("You have now used: " + str(revolutions * 1.5) + " sheets of toilet paper.")
                axis = None
                t_s = time.time()
            #Check if user has not moved for some time.
            t_n = time.time()
            print(t_n - t_s)
            print("Z: " + str(Z))
            print("Axis: " + str(axis))
            print("Revolutions: " + str(revolutions))
            print(name)
            print(number)
            print(revolutions * 1.5)
            if(t_n - t_s > 15):
                sheets = revolutions * 1.5
                custom_str = string_utils.generate_custom_string(sheets)
                outstr = string_utils.generate_output_string(name, sheets)
                body = outstr + custom_str
                dispatch_text(number, body)
                userdata = {"name":name, "sheets":sheets}
                if meme_flag:
                    generate_meme(name, sheets, tweetclient, username, password)
                    dispatch_text(number, "A meme has been generated for you on @toiletdotio, thanks for using!")
                MSG_INFO = mqtt_client.publish("IC.embedded/Useless_System/Data", json.dumps(userdata))
                last_user = get_current_user()
                revolutions, axis = reset(revolutions, axis, rolls)
                return 0
            sleep(0.01)


def on_message(client, userdata, message):
    global current_msg, household, start_flag, roll_flag
    current_msg = str(message.payload.decode("utf-8"))
    if len(current_msg.split()) == 1 and check_for_household():
        start_flag = check_user(current_msg)
    if message.topic == "IC.embedded/Useless_System/Household" and not os.path.isfile('household.json'):
        household = (json.loads(current_msg))
        with open('household.json', 'w') as file:
            json.dump(household, file)
        dispatch_text(household[0]['number'], "How many rolls do you have on first time setup?")
        print("Set up household for first time use")
        print(household)
        MSG = mqtt_client.publish("IC.embedded/Useless_System/Responses",
                                  "Household Setup! You may now use the device.")
    else:
        print("error aryan!")
        print(len(household))
        print(len(current_msg.split()))


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
    global rolls, roll_flag
    # Determine the right reply for this message
    if body == 'MEME':
        meme_flag = True
        resp.message("Time to start rolling, " + get_current_user() + ", we'll handle the memes.")
    elif body == 'NO MEME':
        meme_flag = False
        resp.message("Response acknowledged, you may now roll")
    elif body.split()[0] == "ROLLS":

        rolls = int(body.split()[1])
        with open('rolls.txt', 'w') as file:
            file.write(str(rolls))
        roll_flag = True
        resp.message("Set up IoTP with roll containing " + str(rolls) + " sheets.")
    elif body.split()[0] == "REFILL":
        rolls = int(body.split()[1])
        resp.message("IoTP refilled with " + str(rolls) + " sheets.")
    return str(resp)

mqtt_client.on_message = on_message
mqtt_client.loop_start()

@app.route("/")
def main():
    global last_user, roll_flag
    if not os.path.isfile('household.json'):
        print("Waiting for file")
        while not check_for_household() or not os.path.isfile('rolls.txt'):
            pass
    else:
        with open('household.json') as file:
            global household, rolls
            household = json.load(file)
            with open('rolls.txt') as rolls:
                rolls = int(rolls.readline())
        print("Welcome users")
        print(household)

    if rolls < 10:
        dispatch_text(household[0]['number'], "You're running low on toilet paper, the last user was: " + last_user)

    if rolls == 0:
        dispatch_text(household[0]['number'], "You have run out of toilet paper, please replace your roll. The last user was: " + last_user)

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
        bus = accel_i2c.initialize()
        measure(bus, name, number)



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0') #Test
