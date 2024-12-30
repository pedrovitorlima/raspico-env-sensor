import time
import board
import busio
import json

import adafruit_ltr390
import adafruit_ahtx0
import adafruit_ens160

from mqtt_messenger import MqttClient
from wireless import Network

from secrets import secrets

def send_message(client, sensor_name, value):
    if value is not None:
        body = {
            "device": "pico-env",
            "sensor": sensor_name,
            "reading": value
        }
        
        client.publish(json.dumps(body))

def connect():
    network = Network(secrets['ssid'], secrets['password'])
    pool, ssl_context = network.connect_to_wifi()
    client = MqttClient(secrets['mqtt_broker_address'], 1883, secrets['mqtt_topic'], secrets['mqtt_username'], secrets['mqtt_password'], pool, ssl_context)
    client.connect_to_mqtt()
    return network, client

while True:
    try:
        # TEMP/HUMIDITY SENSOR
        i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
        aht = adafruit_ahtx0.AHTx0(i2c)
        temperature = aht.temperature
        humidity = aht.relative_humidity
        
        # AIR QUALITY - SAME PCB AS PREVIOUS 
        ens160 = adafruit_ens160.ENS160(i2c)
        ens160.temperature_compensation = temperature
        ens160.humidity_compensation = humidity
        aqi = ens160.AQI
        tvoc = ens160.TVOC
        co2 = ens160.eCO2
        
        # RELEASE IC2 BOARD SO THAT THE OTHER SENSOR/PCB CAN USE THAT
        i2c.deinit()
        time.sleep(2)
        
        # UV/LUX SENSOR
        i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
        ltr = adafruit_ltr390.LTR390(i2c)
        light = ltr.light
        uvs = ltr.uvs
        uvi = ltr.uvi
        
        i2c.deinit()
        time.sleep(2)
        
        network, client = connect()
        send_message(client, 'temperature', temperature)
        send_message(client, 'humidity', humidity)
        send_message(client, 'AQI', aqi)
        send_message(client, 'TVOC', tvoc)
        send_message(client, 'eCO2', co2)
        send_message(client, 'ambient_light', light)
        send_message(client, 'UV', uvs)
        send_message(client, 'UVI', uvi)
        network.disconnect()
        
    except Exception as ex:
        print(f"Error type: {type(ex).__name__}")  # Type of exception
        print(f"Error details: {str(ex)}")        # Error message or details
        if hasattr(ex, 'errno'):                 # For OSError and similar
            print(f"Error code: {ex.errno}")
        
    finally:
        if i2c:
            i2c.deinit()
            
    minutes = 5
    time.sleep(minutes * 60)

