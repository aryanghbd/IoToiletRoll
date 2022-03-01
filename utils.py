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




def get_final_sheets():
    return current_sheets

def check_user(username, household):
    for person in household:
        if username == person['name']:
            return True
    return False

def get_number(household):
    name = get_current_user()
    for person in household:
        if name == person['name']:
            return (person['number'])

def get_current_user(household):
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