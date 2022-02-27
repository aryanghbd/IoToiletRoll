import json
from utils import *

def on_message(client, userdata, message):
    global current_msg, household, start_flag
    current_msg = str(message.payload.decode("utf-8"))
    if len(current_msg.split()) == 1 and check_for_household():
        start_flag = check_user(current_msg)
    if message.topic == "IC.embedded/Useless_System/Household" and not os.path.isfile('household.json'):
        household = (json.loads(current_msg))
        with open('household.json', 'w') as file:
            json.dump(household, file)
        print("Set up household for first time use")
        print(household)
        MSG = client.publish("IC.embedded/Useless_System/Responses",
                                  "Household Setup! You may now use the device.")
    else:
        print("error aryan!")
        print(len(household))
        print(len(current_msg.split()))