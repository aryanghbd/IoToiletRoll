import base64
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
import settings

app = Flask(__name__)

#Pass in Twitter Client: Will encrypt these details tonight
username = settings.get_imgflip_username()
password = settings.get_imgflip_password()
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'
#Will also encrypt the following infromation, ideally store them in a credentials document externally
tweetclient = tweepy.Client(consumer_key=base64.b64decode(settings.get_twitter_consumerkey()).decode("utf-8"),
                       consumer_secret=base64.b64decode(settings.get_twitter_consumersecret()).decode("utf-8"),
                       access_token=base64.b64decode(settings.get_twitter_accesstoken()).decode("utf-8"),
                       access_token_secret=base64.b64decode(settings.get_twitter_accesstokensecret()).decode("utf-8"))

#These are Twilio Client tokens
#account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
#auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'

#And here is the MQTT client side tokens.
mqtt_client = mqtt.Client()
mqtt_client.connect("test.mosquitto.org", port=1883)
mqtt_client.subscribe("IC.embedded/Useless_System")
mqtt_client.subscribe("IC.embedded/Useless_System/Household")


#Establish a Twilio Client for SMS functionality
client = Client(base64.b64decode(settings.get_twilio_accountsid()).decode("utf-8"), base64.b64decode(settings.get_twilio_authtoken()).decode("utf-8"))

#These global structures are used in order to manage and pass transmitted info within program context
current_msg = '' #Most recent MQTT message
last_user = '' #Stores in state last user to use device
household = [] #Structure JSON data from MQTT will be dumped into, contains {"name": "x", "number": "123"}
start_flag = False #Flags to indicate state as Flask is a stateless service, to indicate user, configuration choice and SMS responses
meme_flag = None
roll_flag = False
current_sheets = 0.0
rolls = 0.0
#Gathers other values for state

def get_last_user():
    return last_user

def check_meme_flag():
    return meme_flag

def check_roll_flag():
    return roll_flag

def check_start_flag():
    return start_flag

def decrement_sheets(x):
    global rolls
    rolls = rolls - x
    return 0

def get_sheets():
    return rolls

#The following function encapsulates Twilio SMS sending in a more organised functional style.
def dispatch_text(number, content):
    message = client.messages \
        .create(
        body=content,
        from_=settings.get_twilio_phonenumber(),
        to=number
    )
    return 0

#Getter for global value, returns number of sheets.
def get_final_sheets():
    return current_sheets

#When a user is submitted via MQTT, state can only advance if the user is in the valid Household setup.
def check_user(username):
    for person in household:
        if username == person['name']:
            return True
    return False

#Fetches number associated with a valid user
def get_number():
    name = get_current_user()
    for person in household:
        if name == person['name']:
            return (person['number'])

#The last message on MQTT before starting is the name of the user, so this effectively fetches that user, this could have also been saved into a separate state.
def get_current_user():
    return current_msg

#When the user has finished rolling the toilet roll, we need to reset the number of revolutions and sheets taken, as well as update
#the file containing the current number of sheets in the toilet roll, and reset all flags to their pre-use states
#As well as any and all global variables.

#To-Do, to minimise direct tampering with the variables, introduce setters to reduce exposure.
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

#This is an asynchronous function used in a loop to wait for a user to setup a household before
#the device can be used.
def check_for_household():
    if len(household) != 0:
        return True

#This is the main function in the entire device, underpinning all other functions.
#I will comment to explain relevant lines.
def measure(bus, name, number):
    dispatch_text(number, "You may now begin rolling.")
    MSG = mqtt_client.publish("IC.embedded/Useless_System/Responses",
                              f"${name} is now using the device")
    #There is a bit of a latency gap here between sending the HTTP POST and starting, but it is
    #timed well enough.
    global rolls
    last_user = get_last_user()
    while True:
        axis = None
        revolutions = 0
        #Local revolutions and axis flags to make it user specific.
        t_s = time.time()
        #Get starting time.
        while True:
            #Every 0.01s, get the X,Y and Z values.
            X = accel_i2c.get_X(bus)
            Y = accel_i2c.get_Y(bus)
            Z = accel_i2c.get_Z(bus)

            #Halt state if the tracked number of sheets in the device goes below 0
            #Dispatch text to the current user to refill, with SMS 'REFILL X'
            #Where X is the number of rolls, this is saved onto the file and state proceeds.
            if rolls < 0:
                dispatch_text(number, "You have run out of toilet paper, please replace before continuing")
                while rolls < 0:
                    pass

            #A revolution is measured with the following logic:
            #   -At rest, when device is in roll upright, the Z value is the acceleration
            #   due to gravity, i.e approx 9.8ms^-2
            #   -When we have done a half revolution of the roll, the accelerometer is now on
            #   the other vertical end of the toilet roll, measuring a negative value nearing or
            #   approximating to -9.8ms^-2, going against gravity.
            #   -We set a local state flag to indicate we have made a half roll, saving the value
            #   -If our Z value returns to near 9.8, and the axis flag is a negative Z value i.e not none
            #   then we know that we have already made a half rotation earlier, meaning a full rotation has been
            #   made. NOTE: There is the case where you might have gone half up half down, but this is unlikely
            #   in the context of a toilet roll

            #   -When we near 9.8 with a non null axis value, increment the local revolutions value
            #   -One 'roll/revolution' of the toilet paper corresponds to 2 sheets of toilet paper
            #   -However a user may only take one of the two sheets, meaning that an average of 1.5 is generated
            #   -Increment the revolutions while also subtracting 1.5 from the number of sheets the user setup with.

            #   -Reset the axis flag to None again to indicate a new revolution is to be made


            #HOW DO WE KNOW WHEN TO STOP?
            #   -t_n gives the starting time from the user
            #   -t_s gives the current time, we measure the difference between t_s and t_n
            #   -Everytime we increment revolutions, we reset the time for t_s
            #   -Theoretically, everytime we roll again, t_s and t_n are aligned.
            #   -Thus, we know when to stop when t_n - t_s > 15, this means the user has not
            #   revolved the device for 15 seconds, so is likely done.
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
                #The aforementioned end case
                sheets = revolutions * 1.5
                custom_str = string_utils.generate_custom_string(sheets)
                outstr = string_utils.generate_output_string(name, sheets)
                #Generate custom message with random components in header function.
                body = outstr + custom_str #Concatenate the two strings, then text them
                dispatch_text(number, body)
                userdata = {"name":name, "sheets":sheets}
                #JSON format to dispatch through MQTT - Encrypt this later.
                #State from prior is checked, if the user SMS'd "MEME", generate a meme.
                if meme_flag:
                    generate_meme(name, sheets, tweetclient, username, base64.b64decode(password).decode("utf-8"))
                    dispatch_text(number, "A meme has been generated for you on @toiletdotio, thanks for using!")
                MSG_INFO = mqtt_client.publish("IC.embedded/Useless_System/Data", json.dumps(userdata))
                last_user = get_current_user()
                revolutions, axis = reset(revolutions, axis, rolls)
                return 0
                #Reset and await next user.
            sleep(0.01)


def on_message(client, userdata, message):
    global current_msg, household, start_flag, roll_flag
    current_msg = str(message.payload.decode("utf-8"))
    if len(current_msg.split()) == 1 and check_for_household():
        #If we already have a household and there is only one name
        start_flag = check_user(current_msg)
        #Check if the input is a name in the household
    if message.topic == "IC.embedded/Useless_System/Household" and not os.path.isfile('household.json'):
        #If we have not already saved household credentials to a file for local use, do so.
        household = (json.loads(current_msg))
        with open('household.json', 'w') as file:
            json.dump(household, file)
        dispatch_text(household[0]['number'], "How many sheets do you have on first time setup?")
        print("Set up household for first time use")
        print(household)
        #Before starting, text 'head of household', how many sheets they have.
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
    #Establish TwiML parameters.
    resp = MessagingResponse()
    global meme_flag
    global rolls, roll_flag
    #Determine reply and which state flags to alter based on body of message.
    if body == 'MEME':
        meme_flag = True
        resp.message("Time to start rolling, " + get_current_user() + ", we'll handle the memes.")
    elif body == 'NO MEME':
        meme_flag = False
        resp.message("Response acknowledged, you may now roll")
    elif body.split()[0] == "ROLLS":
        #Split message to get the number, cast it to int and write it to rolls.txt.
        rolls = float(body.split()[1])
        with open('rolls.txt', 'w') as file:
            file.write(str(rolls))
        roll_flag = True
        resp.message("Set up IoTP with roll containing " + str(rolls) + " sheets.")
    elif body.split()[0] == "REFILL":
        rolls = float(body.split()[1])
        resp.message("IoTP refilled with " + str(rolls) + " sheets.")
        #No need to write this into the file, as reset will do this at the end of use anyway,
        #Saving unneeded file-writing.
    return str(resp)

mqtt_client.on_message = on_message
mqtt_client.loop_start()

@app.route("/")
def main():
    global last_user, roll_flag, start_flag
    #I would like to convert all of these into getters and setters to avoid global usage.
    if not os.path.isfile('household.json'):
        #If the local file for household hasn't been generated, put it into await state.
        print("Waiting for file")
        while not check_for_household() or not os.path.isfile('rolls.txt'):
            pass
    else:
        #Otherwise, load in local parameters.
        with open('household.json') as file:
            global household, rolls
            household = json.load(file)
            with open('rolls.txt') as rolls:
                rolls = float(rolls.readline())
        print("Welcome users")
        print(household)

    while True:
        print("Now waiting for next user...")
        if rolls < 10:
            if get_last_user() is not '':
                dispatch_text(household[0]['number'], "You're running low on toilet paper, the last user was: " + last_user)
            else:
                dispatch_text(household[0]['number'], "You're running low on toilet paper")
        if rolls == 0:
            #Halt state until refilled.
            if get_last_user() is not '':
                dispatch_text(household[0]['number'],
                          "You have run out of toilet paper, please replace your roll. The last user was: " + last_user)
            else:
                dispatch_text(household[0]['number'], "You have run out of toilet paper, please replace your roll.")
            while rolls == 0:
                pass

        while not start_flag:
            #Wait until a user messages their name via MQTT to start.
            pass
        name = get_current_user()
        number = get_number()
        print("Hello user: " + name)
        print(start_flag)
        print(meme_flag)
        print(test_string)
        dispatch_text(number, "Welcome user: " + name + " Would you be interested in a meme after your session finishes?")
        while check_meme_flag() is None:
            pass
        bus = accel_i2c.initialize()
        measure(bus, name, number)



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0') #Test
