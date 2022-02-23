import paho.mqtt.client as mqtt

account_sid = 'AC552ea4e452978a40ad8d0061fc83e077'
auth_token = '244e9e2bc5d559fbc125ef58a2edc70a'
#client = Client(account_sid, auth_token)

def on_message(client, userdata, message):
    if message.topic == "IC.embedded/Useless_System":
        print(1)
client = mqtt.Client()
client.connect("test.mosquitto.org", port=1883)
client.subscribe("IC.embedded/Useless_System")
client.subscribe("IC.embedded/Useless_System/Data")
client.on_message = on_message
client.loop_start()

def main():
    while True:
        pass

if __name__ == "__main__":
    main()
