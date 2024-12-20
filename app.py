import time
import board
import busio
import adafruit_ltr390
import json
from mqtt_messenger import MqttClient
from wireless import Network

from secrets import secrets


def send_message(client, sensor_name, value):
    if value is not None:
        body = {
            "device": "pico-uvlight",
            "sensor": sensor_name,
            "reading": value
        }
        
        client.publish(json.dumps(body))

network = Network(secrets['ssid'], secrets['password'])
pool, ssl_context = network.connect_to_wifi()

client = MqttClient(secrets['mqtt_broker_address'], 1883, secrets['mqtt_topic'], secrets['mqtt_username'], secrets['mqtt_password'], pool, ssl_context)
client.connect_to_mqtt()

i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
ltr = adafruit_ltr390.LTR390(i2c)
time.sleep(2)

while True:
    try:
        if not network.is_connected():
            print("Wi-Fi disconnected. Reconnecting...")
            network.connect_to_wifi()
            client.connect_to_mqtt()

        send_message(client, 'ambient_light', ltr.light)
        send_message(client, 'UV', ltr.uvs)
        send_message(client, 'UVI', ltr.uvi)
    except Exception as ex:
        print(f"An error occurred: {ex}")
        
    time.sleep(120)

