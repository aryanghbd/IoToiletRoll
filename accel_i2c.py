from utils import *
from sms import *
from meme_utils import *
from mqtt import *

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

def measure(bus, name, number, client):
    dispatch_text(number, "You may now begin rolling.")
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
            print(number)
            print(revolutions * 1.5)
            if(t_n - t_s > 15):
                sheets = revolutions * 1.5
                custom_str = genetate_custom_string(sheets)
                outstr = generate_output_string(name, sheets)
                body = outstr + custom_str
                dispatch_text(number, body)
                userdata = {"name":name, "sheets":sheets}
                if meme_flag:
                    generate_meme(name, sheets)
                    dispatch_text(number, "A meme has been generated for you on @toiletdotio, thanks for using!")
                MSG_INFO = client.publish("IC.embedded/Useless_System/Data", json.dumps(userdata))
                revolutions, axis = reset(revolutions, axis)
                return 0
            sleep(0.01)