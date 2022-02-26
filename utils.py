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
from accel_i2c import *
from sms import *
from mqtt import *

account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
client = Client(account_sid, auth_token)

current_msg = ''
household = []
start_flag = False
meme_flag = None
test_string = ''
current_sheets = 0.0

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
    else:
        return " Roll with awareness!"

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

def dispatch_text(number, content):
    message = client.messages \
        .create(
        body=content,
        from_='+447897016821',
        to=number
    )
    return 0

def synch_wait(time):
    t_s, t_d = time.time()
    while t_d - t_s < 15:
        t_d = time.time()
    return 0