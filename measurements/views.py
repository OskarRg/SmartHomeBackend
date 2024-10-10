# TODO Handle RFID and pinpad data to be saved in the database
# TODO Check if Historical measurements are being saved in the database

# TODO Add every important view from Mateusz's ticket
# TODO Handle MQTT request to check for alarms, I need to know the values and it's ranges
# TODO Add views to urls.py
"""
endpoints to add

# pin change (url)
# light sensitivity (url)
# mqtt to buzzer
# alarm_handling (on/off)
# rfid

"""

import json

import paho.mqtt.client as mqtt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import HistoricalMeasurementFilter
from .models import HistoricalMeasurement
from .serializers import (
    CurrentMeasurementSerializer,
    HistoricalMeasurementSerializer,
    FieldsDictionarySerializer,
    RGBLedValuesSerializer,
    ControlValueSerializer,
    ControlStatusSerializer,
    PinValueSerializer,
)
from .utils import FIELDS_DICTIONARY, MQTT_BROKER, MQTT_PORT, RGBLedValues


class HistoricalMeasurementsListView(generics.ListAPIView):
    serializer_class = HistoricalMeasurementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HistoricalMeasurementFilter
    ordering_fields = ["date"]

    def get_queryset(self):
        measurement_type = self.kwargs["measurement_type"]

        return HistoricalMeasurement.objects.filter(type=measurement_type)


class HistoricalMeasurementDetailView(generics.RetrieveDestroyAPIView):
    queryset = HistoricalMeasurement.objects.all()
    serializer_class = HistoricalMeasurementSerializer


class FieldsDictionaryView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = FieldsDictionarySerializer()

        serialized_data = serializer.serialize(FIELDS_DICTIONARY)

        return Response(serialized_data, status=status.HTTP_200_OK)


class BaseMQTTAPIView(APIView):
    @staticmethod
    def publish_mqtt_message(topic, payload):
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        client.publish(topic, json.dumps(payload), qos=1)
        client.loop_stop()


class LEDControlAPIView(BaseMQTTAPIView):
    def post(self, request, led_number):
        if led_number not in ["1", "2", "3", "4", "5", "6"]:
            return Response(
                {"error": "Invalid LED number"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RGBLedValuesSerializer(data=request.data)
        if serializer.is_valid():
            rgb_values = serializer.validated_data

            self.publish_mqtt_message(f"energy/LED/{led_number}/data", rgb_values)
            if isinstance(
                FIELDS_DICTIONARY["energy"]["leds"][led_number], RGBLedValues
            ):
                return Response(
                    {
                        led_number: FIELDS_DICTIONARY["energy"]["leds"][
                            led_number
                        ].to_dict()
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {led_number: FIELDS_DICTIONARY["energy"]["leds"][led_number]},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GateControlAPIView(BaseMQTTAPIView):
    def post(self, request):
        serializer = ControlStatusSerializer(data=request.data)
        if serializer.is_valid():
            self.publish_mqtt_message(
                "control/gate/motor/control",
                {"value": serializer.validated_data["value"]},
            )
            return Response(
                {"gate_control": FIELDS_DICTIONARY["control"]["gate_control"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoorServoControlAPIView(BaseMQTTAPIView):
    def post(self, request):
        serializer = ControlValueSerializer(data=request.data)
        if serializer.is_valid():
            self.publish_mqtt_message(
                "control/door/servo/control",
                {"value": serializer.validated_data["value"]},
            )
            return Response(
                {
                    "door_servo_control": FIELDS_DICTIONARY["control"][
                        "door_servo_control"
                    ]
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PinChangeAPIView(BaseMQTTAPIView):
    def post(self, request):
        serializer = PinValueSerializer(data=request.data)
        # This needs auth - like to do this you need to give a correct pin earlier
        if serializer.is_valid():
            FIELDS_DICTIONARY["security"]["current_pin"] = serializer.validated_data[
                "value"
            ]
            return Response(
                {"current_pin": FIELDS_DICTIONARY["security"]["current_pin"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LightSensitivityChangeAPIView(BaseMQTTAPIView):
    def post(self, request):
        serializer = ControlValueSerializer(data=request.data)
        if serializer.is_valid():
            FIELDS_DICTIONARY["settings"]["light_sensor_sensitivity"] = (
                serializer.validated_data["value"]
            )
            return Response(
                {"current_pin": FIELDS_DICTIONARY["security"]["current_pin"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FanControlAPIView(BaseMQTTAPIView):
    def post(self, request, fan_number):
        if fan_number not in ["1", "2"]:
            return Response(
                {"error": "Invalid fan number"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ControlStatusSerializer(data=request.data)

        if serializer.is_valid():
            key = f"fan_{fan_number}_control_status"
            self.publish_mqtt_message(
                f"control/fan/{fan_number}/status",
                {"value": serializer.validated_data["value"]},
            )
            return Response(
                {key: FIELDS_DICTIONARY["control"][key]}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolarPanelPositionAPIView(BaseMQTTAPIView):
    def post(self, request):
        serializer = ControlStatusSerializer(data=request.data)
        if serializer.is_valid():
            self.publish_mqtt_message(  # TODO Fix message - change the schema in mqtt to only have one field and boolean
                "control/solar_tracker/servo_vertical/control",
                {"value": serializer.validated_data["value"]},
            )
            return Response(
                {
                    "servo_vertical_control": FIELDS_DICTIONARY["control"][
                        "is_solar_in_safe_position"
                    ]
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
