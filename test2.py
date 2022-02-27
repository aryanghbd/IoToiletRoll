import time
from threading import Thread
import multiprocessing
import os
import json

import paho.mqtt.client as mqtt


path = os.getcwd()

def on_message(client, userdata, message):
    global current_msg, household, start_flag
    current_msg = str(message.payload.decode("utf-8"))

    if message.topic == "IC.embedded/Useless_System/Household" and not os.path.isfile('household.json'):
        household = (json.loads(current_msg))
        with open('household.json', 'w') as file:
            json.dump(household, file)
        MSG = mqtt_client.publish("IC.embedded/Useless_System/Responses", "Household Setup! You may now use the device.")

mqtt_client = mqtt.Client()
mqtt_client.connect("test.mosquitto.org", port=1883)
mqtt_client.subscribe("IC.embedded/Useless_System")
mqtt_client.subscribe("IC.embedded/Useless_System/Household")
mqtt_client.on_message = on_message
mqtt_client.loop_start()

if not os.path.isfile('household.json'):
    print("Waiting for file")
    while not os.path.isfile('household.json'):
        pass
    print("Set up successfully")
    with open('household.json') as file:
        household = json.load(file)
    print("Set up with users, ")
    print(household)
else:
    with open('household.json') as file:
        household = json.load(file)
    print("Welcome back, users")
    print(household)