import paho.mqtt.client as mqtt
import json
from datetime import datetime
from measurements.models import CurrentMeasurement, HistoricalMeasurement, Home


# =================== FABRYKA HANDLERÓW =================== #

class MeasurementHandlerFactory:
    """
    Fabryka handlerów do obsługi różnych tematów MQTT.
    """

    @staticmethod
    def get_handler(topic):
        if topic == "sensor/current_measurements":
            return CurrentMeasurementsHandler()
        elif topic == "sensor/history_measurements":
            return HistoryMeasurementsHandler()
        else:
            return None


# =================== HANDLERY TEMATÓW =================== #

class CurrentMeasurementsHandler:
    """
    Handler do obsługi wiadomości dla tematu 'sensor/current_measurements'.
    """

    def handle(self, data):
        try:
            room_id = data.get('room_id')
            measurement_type = data.get('type')
            value = data.get('value')
            timestamp = data.get('date', datetime.now().isoformat())

            room = Home.objects.get(id=room_id)

            # Aktualizacja lub utworzenie rekordu w CurrentMeasurement
            current_measurement, created = CurrentMeasurement.objects.update_or_create(
                room=room,
                type=measurement_type,
                defaults={'value': value, 'date': datetime.fromisoformat(timestamp)}
            )

            if created:
                print(f"Utworzono nowy bieżący pomiar dla pokoju: {room.name}")
            else:
                print(f"Zaktualizowano bieżący pomiar dla pokoju: {room.name}")

        except Exception as e:
            print(f"Błąd przetwarzania current_measurements: {e}")


class HistoryMeasurementsHandler:
    """
    Handler do obsługi wiadomości dla tematu 'sensor/history_measurements'.
    """

    def handle(self, data):
        try:
            room_id = data.get('room_id')
            measurement_type = data.get('type')
            value = data.get('value')
            timestamp = data.get('date', datetime.now().isoformat())

            room = Home.objects.get(id=room_id)

            HistoricalMeasurement.objects.create(
                room=room,
                type=measurement_type,
                value=value,
                date=datetime.fromisoformat(timestamp)
            )

            print(f"Zapisano pomiar dla pokoju: {room.name}")

        except Exception as e:
            print(f"Błąd przetwarzania history_measurements: {e}")


# =================== MQTT CALLBACKS =================== #

def on_connect(client, userdata, flags, rc):
    """
    Callback, gdy klient połączy się z brokerem MQTT.
    Subskrybuje wszystkie wymagane tematy.
    """
    print(f"Połączono z MQTT Brokerem: {rc}")
    client.subscribe("sensor/#")  # Subskrybuje wszystkie tematy zaczynające się od "sensor/"


def on_message(client, userdata, msg):
    """
    Callback, gdy klient otrzyma wiadomość z brokera MQTT.
    Na podstawie tematu wybiera odpowiedni handler.
    """
    print(f"Otrzymano wiadomość z tematu: {msg.topic}")
    try:
        # Parsowanie wiadomości JSON
        data = json.loads(msg.payload)

        # Fabryka zwraca odpowiedni handler na podstawie tematu
        handler = MeasurementHandlerFactory.get_handler(msg.topic)

        if handler:
            handler.handle(data)
        else:
            print(f"Brak handlera dla tematu: {msg.topic}")

    except Exception as e:
        print(f"Błąd przetwarzania wiadomości: {e}")


# =================== URUCHOMIENIE KLIENTA MQTT =================== #

def start_mqtt_client():
    """
    Funkcja startująca klienta MQTT.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Połącz z brokerem MQTT (zmień adres brokera, jeśli potrzeba)
    client.connect("localhost", 1883, 60)

    # Utrzymuj połączenie w pętli
    client.loop_forever()


if __name__ == "__main__":
    start_mqtt_client()
