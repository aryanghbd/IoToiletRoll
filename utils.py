import os
import time

import smbus2
from time import sleep
from twilio.rest import Client
from threading import Timer
import paho.mqtt.client as mqtt
import json

#Global client in order to pass into functions.


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

def set_max(rev):
    max = rev
    return 0

def get_max():
    return max

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
    global current_msg, start_flag
    current_msg = ""
    start_flag = False
    return revolutions, axis

def custom_msg(n):
    if 1 < n < 5:
        return "Didn't use much did you?"
    if 6 < n < 10:
        return "Damn."

def check_for_household():
    if len(household) != 0:
        return True

def await_users():
    print("Now waiting for user input..")
    while not start_flag:
        pass

def measure(bus, name, number):
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
            if(t_n - t_s > 15):
                custom_str = ""
                message = client.messages \
                    .create(
                    body="Hi, " + name + ". This time you took " + str(revolutions * 1.5) + " sheets of toilet paper. " #+ custom_msg(revolutions * 1.5),
                    from_='+447897016821',
                    to=number
                )
                MSG_INFO = mqtt_client.publish("IC.embedded/Useless_System/Data", "User used " + str(revolutions * 1.5) + " sheets.")
                revolutions, axis = reset(revolutions, axis)
                return 0
            sleep(0.01)

def on_message(client, userdata, message):
    global current_msg, household, start_flag
    current_msg = str(message.payload.decode("utf-8"))
    if len(current_msg.split()) == 1 and len(household) != 0:
        start_flag = check_user(current_msg)
    else:
        if message.topic == "IC.embedded/Useless_System/Household":
            household = (json.loads(current_msg))
            MSG = mqtt_client.publish("IC.embedded/Useless_System/Responses", "Household Setup! You may now use the device.")

mqtt_client = mqtt.Client()
mqtt_client.connect("test.mosquitto.org", port=1883)
mqtt_client.subscribe("IC.embedded/Useless_System")
mqtt_client.subscribe("IC.embedded/Useless_System/Household")
mqtt_client.on_message = on_message
mqtt_client.loop_start()
def main():
    if not check_for_household():
        print("Waiting for household to be input")
        while not check_for_household():
            pass
    print("Household setup! You may now proceed to use the toilet.io device")
    while True:
        print("Now waiting for next user...")
        while not start_flag:
            pass
        name = get_current_user()
        number = get_number()
        print("Hello user: " + name)
        bus = initialize()
        measure(bus, name, number)



if __name__ == "__main__":
    main()