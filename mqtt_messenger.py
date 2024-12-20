import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time
  
class MqttClient:

  def __init__(self, broker, port, topic, username, password, pool, ssl_context):
    self.__client = MQTT.MQTT(
        broker=broker,
        port=port,
        client_id="light-sensor",
        username=username,
        password=password,
        socket_pool=pool,
        ssl_context=ssl_context
    )

    self.__topic = topic
    self.__client.on_connect = on_connect
    self.__client.on_publish = on_publish

  def connect_to_mqtt(self):
    while True:
      try:
          self.__client.connect()
          print("Reconnected to MQTT broker")
          break
      except Exception as ex:
          print(f"Failed to connect to MQTT: {ex}. Retrying in 5 seconds...")
          time.sleep(5)
  
  def publish(self, message):
    self.__client.publish(self.__topic, message)
  
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

def on_publish(mqtt_client, userdata, topic, pid):
  print("\tPublished a message to: ", topic)
