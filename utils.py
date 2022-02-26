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

#ESTABLISHING CONSTANT REGISTERS#

device_addr = 0x18

ctrl_reg1 = 0x20 #These registers are how we initialise
ctrl_reg4 = 0x00

x_reg_high = 0x29 #These registers give the high and low nibbles of the relevant axis information
x_reg_low = 0x28

y_reg_high = 0x2B
y_reg_low = 0x2A

z_reg_high = 0x2D
z_reg_low = 0x2C
max = 0
#Helpful global variables
#bus = smbus2.SMBus(1)
#bus.write_byte_data(0x18, 0x20, 0xA7) #Run accelerometer at 100Hz
#bus.write_byte_data(0x18, 0x23, 0x00)
account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
client = Client(account_sid, auth_token)

current_msg = ''
household = []
start_flag = False
meme_flag = None
test_string = ''
current_sheets = 0.0

def get_final_sheets():
    return current_sheets

def generate_meme_text(id, name, number):
    text0 = ''
    text1 = ''
    if id == 1:
            text0 = name + " using excessive amounts of toilet paper"
            text1 = name + " using toilet paper in moderation"
    if id == 2:
            text0 = name + " using up " + str((int)(number)) + " sheets of toilet paper"
            text1 = name + " planting " + str((int)(number)) + " trees instead"
    if id == 3:
            text0 = name + " being a friend to the environment"
            text1 = name + " using up " + str((int)(number)) + " sheets instead"
    if id == 4:
            text0 = name + " using " + str((int)(number)) + " sheets of toilet paper"
            text1 = name + " paying up for next week's TP budget"
    if id == 5:
            text0 = name + " being a friend to the trees"
            text1 = name
    return text0, text1

def generate_meme(name, number):
#Fetch the available memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
    #List all the memes
    URL = 'https://api.imgflip.com/caption_image'
    memes = [1,2,3,4,5]
    id = random.choice(memes)
    text0, text1 = generate_meme_text(id, name, number)
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':text0,
        'text1':text1
    }
    response = requests.request('POST',URL,params=params).json()
    url = response['data']['url']


    # # Replace the text with whatever you want to Tweet about
    responses = tweetclient.create_tweet(text= "Looks like someone just used the loo and made a meme! " + url)
    responses = tweetclient.create_tweet
    print(responses)
    return 0

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

def initialize():
    bus = smbus2.SMBus(1)
    bus.write_byte_data(device_addr, ctrl_reg1, 0xA7) #A7 allows 100Hz standard operation enabling all 3 axes
    bus.write_byte_data(device_addr, ctrl_reg4, 0x00) #Standard operation

    print("Starting Up toilet.io...Please Wait")
    sleep(2)
    return bus

def normalize(bus, device, register):
    lsb = bus.read_byte_data(device, register)
    msb = bus.read_byte_data(device, register + 1)
    res = (msb << 8 | lsb)
    if res > 32768:
        res = res - 65536
    return (res/16380) * 9.8

def get_X(bus):
    return normalize(bus, device_addr, x_reg_low)

def get_Y(bus):
    return normalize(bus, device_addr, y_reg_low)

def get_Z(bus):
    return normalize(bus, device_addr, z_reg_low)

def reset(revolutions, axis):
    print("Sorry, resetting now!")
    revolutions = 0
    axis = None
    global current_msg, start_flag, meme_flag, current_sheets
    current_msg = ""
    start_flag = False
    meme_flag = None
    current_sheets = 0.0
    return revolutions, axis

def check_for_household():
    if len(household) != 0:
        return True

def generate_output_string(name, number):
    greetings = ["What's up, ", "How's it hanging, or should I say... how's it rolling, ", "Greetings from the toilet, ", "All done, ", "Nice flush, "]
    greeting = random.choice(greetings)
    return greeting + name + ". This time round you used " + str(number) + " sheets of toilet paper by our estimates."

def genetate_custom_string(number):
    if 1 < number < 3:
        return " That was barely anything! Were you rolling for fun?"
    if 4 < number < 10:
        return " Nice usage! Keep up the moderate usage to help the environment one toilet trip at a time."
    if 11 < number < 25:
        return " Are you flushing down a textbook? At " + str(number * 0.12) + "m, you rolled a small child or a baseball bat, do better."
    if 26 < number < 40:
        return " God damn."
def dispatch_text(number, content):
    message = client.messages \
        .create(
        body=content,
        from_='+447897016821',
        to=number
    )
    return 0

def measure(bus, name, number):
    dispatch_text(number, "You may now begin rolling.")
    while True:
        #lastZ = None
        axis = None
        revolutions = 0
        #current_max = get_max()
        t_s = time.time()
        while True:
            X = get_X(bus)
            Y = get_Y(bus)
            Z = get_Z(bus)
            if Z < -7.5 and axis == None:
                axis = Z
            if Z > 8 and axis != None:
                revolutions = revolutions + 1
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
                custom_str = genetate_custom_string(sheets)
                outstr = generate_output_string(name, sheets)
                body = outstr + custom_str
                dispatch_text(number, body)
                userdata = {"name":name, "sheets":sheets}
                if meme_flag:
                    generate_meme(name, sheets)
                    dispatch_text(number, "A meme has been generated for you on @toiletdotio, thanks for using!")
                MSG_INFO = mqtt_client.publish("IC.embedded/Useless_System/Data", json.dumps(userdata))
                revolutions, axis = reset(revolutions, axis)
                return 0
            sleep(0.01)

def synch_wait(time):
    t_s, t_d = time.time()
    while t_d - t_s < 15:
        t_d = time.time()
    return 0
def on_message(client, userdata, message):
    global current_msg, household, start_flag
    current_msg = str(message.payload.decode("utf-8"))
    if len(current_msg.split()) == 1 and check_for_household():
        start_flag = check_user(current_msg)
    if message.topic == "IC.embedded/Useless_System/Household" and not os.path.isfile('household.json'):
        household = (json.loads(current_msg))
        with open('household.json', 'w') as file:
            json.dump(household, file)
        print("Set up household for first time use")
        print(household)
        MSG = mqtt_client.publish("IC.embedded/Useless_System/Responses",
                                  "Household Setup! You may now use the device.")
    else:
        print("error aryan!")
        print(len(household))
        print(len(current_msg.split()))
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
        measure(bus, name, number)



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0') #Test