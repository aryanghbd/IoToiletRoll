import paho.mqtt.client as mqtt
import requests
import os
from twilio.rest import Client
msg = ""
def on_message(client, userdata, message):
    mes = str(message.payload.decode("utf-8"))
    print(mes)



account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
#client = Client(account_sid, auth_token)
client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
client.subscribe("IC.embedded/Useless_System")
client.on_message = on_message
while True:
    client.loop_start()

#Isolate the means of error checking

#ToDo: Trigger words from MQTT to get the Pi to start seeking

#if((mqtt.error_string(MSG_INFO.rc))) == "No error.":
#    print("Sent!")

