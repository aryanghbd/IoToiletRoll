import smbus2
from time import sleep

import sms
from meme import generate_meme_text, generate_meme
import time
from sms import dispatch_text
from string_utils import *

device_addr = 0x18

ctrl_reg1 = 0x20 #These registers are how we initialise
ctrl_reg4 = 0x00

x_reg_high = 0x29 #These registers give the high and low nibbles of the relevant axis information
x_reg_low = 0x28

y_reg_high = 0x2B
y_reg_low = 0x2A

z_reg_high = 0x2D
z_reg_low = 0x2C

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
