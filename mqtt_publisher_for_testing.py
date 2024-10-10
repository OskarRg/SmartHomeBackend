import paho.mqtt.client as mqtt
import json

from measurements.utils import TOPIC_TO_FIELD_MAP

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smarthome/energy/intensity_sensor/data"


def publish_message(client, topic):
    topic = f"smarthome/{topic}"
    message = {
        "value": 1.0
    }

    if "LED" in topic:
        led_number = topic.split("/")[-2]
        message = {
            "red": 0,
            "green": 0,
            "blue": 0
        }

    elif "RFID" in topic:
        message = {
            "value": "1234567890"
        }
    elif "pinpad" in topic:
        message = {
            "value": "D U P A"
        }

    client.publish(topic, json.dumps(message), qos=0)
    print(f"Opublikowano wiadomość na topic: {topic} - {message}")


def publish_to_all_topics():
    client = mqtt.Client()

    client.connect(mqtt_broker, mqtt_port)

    for topic in TOPIC_TO_FIELD_MAP.keys():
        publish_message(client, topic)

    client.disconnect()


if __name__ == "__main__":
    publish_to_all_topics()
