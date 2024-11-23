import datetime
import json

import paho.mqtt.client as mqtt
from django.utils import timezone
from django.db import models

from measurements.models import HistoricalMeasurement, RFIDCard, EnergyProductionMeasurement, \
    EnergyConsumptionMeasurement
from measurements.utils import (
    RGBLedValues,
    FIELDS_DICTIONARY,
    TOPIC_TO_FIELD_MAP,
    CurrentMeasurement,
    rfid_manager,
    MQTT_BROKER,
    MQTT_PORT, EnergyMeasurement,
)


class BaseHandler:
    def handle(self, topic: str, payload: dict):
        raise NotImplementedError("Handler must implement the 'handle' method")

    @staticmethod
    def publish_mqtt_message(topic, payload):
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        client.publish(topic, json.dumps(payload), qos=1)
        client.loop_stop()


class DefaultHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        print("DEFAULT HANDLER")
        value = payload.get("value")
        print(payload)
        if value in (None, "") and not isinstance(value, int):
            print(f"The value from the topic {topic} is missing")
            return

        field_path = TOPIC_TO_FIELD_MAP[topic]
        if field_path is None:
            print(f"Topic {topic} is not handled.")
            return

        current_dict = FIELDS_DICTIONARY
        for key in field_path[:-1]:
            current_dict = current_dict[key]

        current_dict[field_path[-1]] = value


class SecurityHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        print("SECURITY HANDLER")
        value = payload.get("value")
        alarm_on = payload.get("alarm_on")
        print(payload)
        if value in (None, "") and not isinstance(value, int):
            print(f"The value from the topic {topic} is missing")
            return

        field_path = TOPIC_TO_FIELD_MAP[topic]
        if field_path is None:
            print(f"Topic {topic} is not handled.")
            return

        current_dict = FIELDS_DICTIONARY
        for key in field_path[:-1]:
            print("key: ", key)

            current_dict = current_dict[key]

        current_dict[field_path[-1]] = {"value": value, "alarm_on": alarm_on}


class LEDHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        led_number = int(topic.split("/")[-2])
        red = payload["red"]
        green = payload["green"]
        blue = payload["blue"]

        if red is None or green is None or blue is None:
            print(f"LED RGB values are incomplete from topic: {topic}")
            return

        rgb_value = RGBLedValues(led_number, red, green, blue)

        FIELDS_DICTIONARY["energy"]["leds"][str(led_number)] = rgb_value


"""
class RFIDHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        value = payload["value"]
        if value is None:
            print(f"No RFID value from the topic: {topic}")
            return
        FIELDS_DICTIONARY["security"]["rfid_data"] = value
"""


class PinPadHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        code = payload.get("value")
        if code == FIELDS_DICTIONARY["security"]["current_pin"]:
            print("Correct pin entered. Door opening i need to implement it.")
            self.publish_mqtt_message("smarthome/control/door/lock/status", {"value": 0})
        else:
            print(f"Incorrect pin entered. Not opening the door. pin: {code}, current pin: {FIELDS_DICTIONARY['security']['current_pin']}")


class RFIDHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        code = payload.get("value")

        if code is None:
            print(f"RFID code is missing from the topic: {topic}")
            return

        pending_rfid_owner = rfid_manager.get_pending_rfid_owner()

        rfid_card = RFIDCard.objects.filter(code=code).first()
        # TODO Is every card code unique? If not, we need to check for owner.

        if rfid_card:
            print(f"RFID card {code} recognized. Unlocking the door...")

            self.publish_mqtt_message(
                "smarthome/control/door/lock/status", {"value": 0}
            )
        else:
            print("rfid_card", rfid_card)
            if pending_rfid_owner:
                try:
                    RFIDCard.objects.create(owner=pending_rfid_owner, code=code)
                    print(
                        f"Added new RFID card with code {code} for owner {pending_rfid_owner}."
                    )

                    rfid_manager.set_pending_rfid_owner(None)
                except Exception as e:
                    print(f"Error saving RFID card: {e}")
            else:
                print(f"No pending RFID request. Ignoring card with code {code}.")


def save_measurement_to_db(measurement_type: str, value: float, model: type[models.Model]):
    if measurement_type is None:
        print(f"Measurement type {measurement_type} is not recognized for database.")
        return

    try:

        naive_datetime = datetime.datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        model.objects.create(
            type=measurement_type, value=value, date=aware_datetime
        )
    except Exception as e:
        print(f"Error saving measurement to database: {e}")


class EnvironmentMeasurementHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        value = payload.get("value")
        measurement_type = topic.split("/")[-2]
        measurement_type = SENSOR_TO_TYPE_MAP[measurement_type]
        if value is None:
            print(f"No value from the topic: {topic}")
            return

        field_path = TOPIC_TO_FIELD_MAP[topic]
        if field_path is None:
            print(f"Topic {topic} is not handled.")
            return
        naive_datetime = datetime.datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        measurement = CurrentMeasurement(
            measurement_type=measurement_type, value=value, date=aware_datetime
        )
        current_dict = FIELDS_DICTIONARY
        for key in field_path[:-1]:
            current_dict = current_dict[key]

        current_dict[field_path[-1]] = measurement
        save_measurement_to_db(measurement_type, value, model=HistoricalMeasurement)


class EnergyProductionMeasurementHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        value = payload.get("value")
        measurement_type = topic.split("/")[-2]
        measurement_type = SENSOR_TO_TYPE_MAP[measurement_type]
        if value is None:
            print(f"No value from the topic: {topic}")
            return

        field_path = TOPIC_TO_FIELD_MAP[topic]
        if field_path is None:
            print(f"Topic {topic} is not handled.")
            return
        naive_datetime = datetime.datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        measurement = EnergyMeasurement(
            measurement_type=measurement_type, value=value, date=aware_datetime
        )
        current_dict = FIELDS_DICTIONARY
        for key in field_path[:-1]:
            current_dict = current_dict[key]

        current_dict[field_path[-1]] = measurement
        save_measurement_to_db(measurement_type, value, model=EnergyProductionMeasurement)


class EnergyConsumptionMeasurementHandler(BaseHandler):
    def handle(self, topic: str, payload: dict):
        value = payload.get("value")
        measurement_type = topic.split("/")[-2]
        measurement_type = SENSOR_TO_TYPE_MAP[measurement_type]
        if value is None:
            print(f"No value from the topic: {topic}")
            return

        field_path = TOPIC_TO_FIELD_MAP[topic]
        if field_path is None:
            print(f"Topic {topic} is not handled.")
            return
        naive_datetime = datetime.datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        measurement = EnergyMeasurement(
            measurement_type=measurement_type, value=value, date=aware_datetime
        )
        current_dict = FIELDS_DICTIONARY
        for key in field_path[:-1]:
            current_dict = current_dict[key]

        current_dict[field_path[-1]] = measurement
        save_measurement_to_db(measurement_type, value, model=EnergyConsumptionMeasurement)


TOPIC_HANDLER_MAP = {
    "security/RFID/data": RFIDHandler(),
    "energy/LED/1/data": LEDHandler(),
    "energy/LED/2/data": LEDHandler(),
    "energy/LED/3/data": LEDHandler(),
    "energy/LED/4/data": LEDHandler(),
    "energy/LED/5/data": LEDHandler(),
    "energy/LED/6/data": LEDHandler(),
    "environment/multi_sensor/temperature/data": EnvironmentMeasurementHandler(),
    "environment/multi_sensor/humidity/data": EnvironmentMeasurementHandler(),
    "environment/multi_sensor/pressure/data": EnvironmentMeasurementHandler(),
    "environment/gas_sensor/data": EnvironmentMeasurementHandler(),
    "energy/energy_consumption/current/data": EnergyConsumptionMeasurementHandler(), # TU
    "energy/energy_consumption/power/data": EnergyConsumptionMeasurementHandler(),
    "energy/energy_consumption/voltage/supply/data": EnergyConsumptionMeasurementHandler(),
    "energy/energy_consumption/voltage/bus/data": EnergyConsumptionMeasurementHandler(),
    "energy/energy_production/current/data": EnergyProductionMeasurementHandler(),
    "energy/energy_production/power/data": EnergyProductionMeasurementHandler(),
    "energy/energy_production/voltage/supply/data": EnergyProductionMeasurementHandler(),
    "energy/energy_production/voltage/bus/data": EnergyProductionMeasurementHandler(),
    "security/tilt_sensor/status": SecurityHandler(),
    "security/radiation_sensitive/status": SecurityHandler(),
    "security/buzzer/status": SecurityHandler(),
    "security/alarm_armed/status": PinPadHandler(),
    "security/flame_sensor/status": SecurityHandler(),
    "security/PIR/1/status": SecurityHandler(),
    "security/PIR/2/status": SecurityHandler(),
}

SENSOR_TO_TYPE_MAP = {
    "temperature": "T",
    "humidity": "H",
    "pressure": "P",
    "gas_sensor": "G",
    "bus": "B",
    "current": "C",
    "power": "P",
    "supply": "S",
}


def on_message(client, userdata, message):
    print("AA: ", message.topic)
    topic = "/".join(message.topic.split("/")[1:])
    payload = json.loads(message.payload)
    print(f"Received message on topic: {topic}")
    if topic in TOPIC_HANDLER_MAP:
        handler = TOPIC_HANDLER_MAP[topic]
        handler.handle(topic, payload)
    else:
        default_handler = DefaultHandler()
        default_handler.handle(topic, payload)


def start_mqtt_client():
    client = mqtt.Client()
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    for topic in TOPIC_TO_FIELD_MAP.keys():
        smarthome_topic = f"smarthome/{topic}"
        client.subscribe(f"{smarthome_topic}")
        print(f"Subscribed to topic: {smarthome_topic}")

    client.loop_start()


if __name__ == "__main__":
    start_mqtt_client()
