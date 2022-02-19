import paho.mqtt.client as mqtt
import requests
import os

client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
MSG_INFO = client.publish("IC.embedded/Useless_System", "test")

#Isolate the means of error checking

#ToDo: Trigger words from MQTT to get the Pi to start seeking

if((mqtt.error_string(MSG_INFO.rc))) == "No error.":
    print("Sent!")

