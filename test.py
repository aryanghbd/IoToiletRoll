import paho.mqtt.client as mqtt
import json
import pandas as pd

import requests
import os
from twilio.rest import Client
current_msg = ''
household = {}

active_user = False

current_sheets = 0.0

def get_final_sheets():
    return current_sheets

def check_user(username):
    for person in household:
        if username == person['name']:
            return True
    return False

def get_name_number():
    for person in household:
        if current_msg == person['name']:
            return (person['name'], person['number'])
    return "No User Found"

def on_message(client, userdata, message):
    global current_msg, household, active_user
    current_msg = str(message.payload.decode("utf-8"))
    if len(current_msg.split()) == 1 and len(household) != 0:
        active_user = check_user(current_msg)
    else:
        (firstWord, rest) = current_msg.split(maxsplit=1)
        if firstWord == "HOUSEHOLD":
            household = (json.loads(rest))

account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
#client = Client(account_sid, auth_token)
client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
client.subscribe("IC.embedded/Useless_System")
client.on_message = on_message
client.loop_start()


def main():
    while True:
        if len(household) != 0:
            print("Household setup! You may now proceed to use the toilet.io device")

            while True:
                if active_user:
                    (name, number) = get_name_number()
                    print("Hello " + name)
                    print(number)
                    #print(household['members'][index]['number'])
                    return 0
        else:
            pass


if __name__ == "__main__":
    main()
#Isolate the means of error checking

#ToDo: Trigger words from MQTT to get the Pi to start seeking

#if((mqtt.error_string(MSG_INFO.rc))) == "No error.":
#    print("Sent!")

