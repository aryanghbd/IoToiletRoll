import os
import time

import smbus2
from time import sleep
from twilio.rest import Client
from threading import Timer
import paho.mqtt.client as mqtt

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
household = ['Aryan', 'Holly', 'Brandon', 'Osman']

def on_message(client, userdata, message):
    global current_msg
    current_msg = str(message.payload.decode("utf-8"))

def get_current_message():
    return current_msg
#Getter function for ease of use

def reset():
    revolutions = 0
    axis = None

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

def check(revolutions, axis):
    print("Sorry, resetting now!")
    revolutions = 0
    axis = None
    return revolutions, axis

def custom_msg(n):
    if 1 < n < 5:
        return "Didn't use much did you?"
    if 6 < n < 10:
        return "Damn."

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.connect("test.mosquitto.org", port=1883)
    mqtt_client.subscribe("IC.embedded/Useless_System")
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
    while True:
        name = get_current_message()
        if name in household:
            print("Hello user: " + name)
            bus = initialize()
            #lastZ = None
            print("Spin!")
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
                if(t_n - t_s > 15):
                    custom_str = ""
                    message = client.messages \
                        .create(
                            body="This time you took " + str(revolutions * 1.5) + " sheets of toilet paper. " + custom_msg(revolutions * 1.5),
                            from_='+447897016821',
                            to='+447711223376'
                        )
                    #MSG_INFO = mqtt_client.publish("IC.embedded/Useless_System", "User used " + str(revolutions * 1.5) + " sheets.")
                    revolutions, axis = check(revolutions, axis)
                    break
                sleep(0.01)

if __name__ == "__main__":
    main()