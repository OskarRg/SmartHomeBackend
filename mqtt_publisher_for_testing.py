import paho.mqtt.client as mqtt
import json

# Ustawienia brokera MQTT
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "sensor/measurements"

# Funkcja publikująca wiadomość
def publish_message():
    client = mqtt.Client()

    # Połącz się z brokerem
    client.connect(mqtt_broker, mqtt_port)

    # Przykładowa wiadomość w formacie JSON
    message = {
        "room_id": 1,
        "type": "T",
        "value": 69.5,
        "date": "2024-10-05T12:34:56"
    }

    # Publikowanie wiadomości
    client.publish(mqtt_topic, json.dumps(message), qos=1)

    print(f"Opublikowano wiadomość: {message}")
    # Zamknięcie połączenia
    client.disconnect()


if __name__ == "__main__":

    publish_message()
