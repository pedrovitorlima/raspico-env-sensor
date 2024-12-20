import time
import wifi
import ssl

import socketpool

class Network:

    def __init__(self, ssid, password):
        self.__ssid = ssid
        self.__password = password
    
    def connect_to_wifi(self):
        while True:
            try:
                print(f'Connecting to Wi-Fi {self.__ssid}...')
                wifi.radio.connect(self.__ssid, self.__password)
                print(f"Connected to Wi-Fi: {wifi.radio.ipv4_address}")

                return socketpool.SocketPool(wifi.radio), ssl.create_default_context()
            except Exception as e:
                print(f"Failed to connect: {e}. Retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying

    def is_connected(self):
        return wifi.radio.ipv4_address == None