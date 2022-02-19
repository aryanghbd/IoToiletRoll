import paho.mqtt.client as mqtt
import requests
import os
from twilio.rest import Client

account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
client = Client(account_sid, auth_token)
#client.connect("test.mosquitto.org", port=1883)
#MSG_INFO = client.publish("IC.embedded/Useless_System", "test")
message = client.messages.create(
    body="You are taking a hench shit",
    from_='+447897016821',
    to='+447711223376'
)
#Isolate the means of error checking

#ToDo: Trigger words from MQTT to get the Pi to start seeking

#if((mqtt.error_string(MSG_INFO.rc))) == "No error.":
#    print("Sent!")

