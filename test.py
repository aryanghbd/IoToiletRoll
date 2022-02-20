import paho.mqtt.client as mqtt
import requests
import os
from twilio.rest import Client
current_msg = ''
def on_message(client, userdata, message):
    global current_msg
    current_msg = str(message.payload.decode("utf-8"))

account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
#client = Client(account_sid, auth_token)
client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
client.subscribe("IC.embedded/Useless_System")
client.on_message = on_message
client.loop_start()
household = ['Aryan', 'Holly', 'Brandon', 'Osman']

while True:
    if current_msg in household:
        print("You're in the household, " + current_msg)
        for i in range(10):
            print(i)
        break


#Isolate the means of error checking

#ToDo: Trigger words from MQTT to get the Pi to start seeking

#if((mqtt.error_string(MSG_INFO.rc))) == "No error.":
#    print("Sent!")

