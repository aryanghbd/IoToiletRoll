import os

import smbus2
from time import sleep
from twilio.rest import Client
from threading import Timer

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

#Helpful global variables
#bus = smbus2.SMBus(1)
#bus.write_byte_data(0x18, 0x20, 0xA7) #Run accelerometer at 100Hz
#bus.write_byte_data(0x18, 0x23, 0x00)
account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
client = Client(account_sid, auth_token)

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

def main():
    bus = initialize()
    lastZ = None
    print("Spin!")
    axis = None
    revolutions = 0
    while True:
        X = get_X(bus)
        Y = get_Y(bus)
        Z = get_Z(bus)
        print(lastZ)
        if Z == lastZ:
            t = Timer(5, check, args=(revolutions, axis), kwargs=None)
        if Z < -7.5 and axis == None:
            axis = Z
        if Z > 8 and axis != None:
            revolutions = revolutions + 1
            print("Rolled! Number of revolutions: " + str(revolutions))
            print("You have now used: " + str(revolutions * 1.5) + " sheets of toilet paper.")
            axis = None
            message = client.messages \
                .create(
                    body="You have currently taken " + str(revolutions * 1.5) + " sheets of toilet paper.",
                    from_='+447897016821',
                    to='+447711223376'
                )
        lastZ = Z
        print(Z)
        #Check if user has not moved for some time.
        sleep(0.01)

if __name__ == "__main__":
    main()