from rest_framework import serializers

from .models import HistoricalMeasurement
from .utils import RGBLedValues, CurrentMeasurement


class FieldsDictionarySerializer:
    def serialize(self, data):
        if isinstance(data, dict):
            return {key: self.serialize(value) for key, value in data.items()}
        elif isinstance(data, CurrentMeasurement):
            return self.serialize_current_measurement(data)
        elif isinstance(data, RGBLedValues):
            return self.serialize_rgb_led_values(data)
        else:
            return data

    @staticmethod
    def serialize_current_measurement(obj: CurrentMeasurement):
        return {
            "type": obj.measurement_type,
            "value": obj.value,
            "date": obj.date.isoformat(),
        }

    @staticmethod
    def serialize_rgb_led_values(obj: RGBLedValues):
        return {
            "led_number": obj.led_number,
            "red": obj.red,
            "green": obj.green,
            "blue": obj.blue,
        }


class RGBLedValuesSerializer(serializers.Serializer):
    red = serializers.IntegerField(required=True)
    green = serializers.IntegerField(required=True)
    blue = serializers.IntegerField(required=True)


class ControlStatusSerializer(serializers.Serializer):
    value = serializers.BooleanField(required=True)


class PinValueSerializer(serializers.Serializer):
    old_pin = serializers.CharField(
        # required=True
    )  # Check if this is correct field type
    new_pin = serializers.CharField()


class ControlValueSerializer(serializers.Serializer):
    value = serializers.FloatField(required=True)


class CurrentMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentMeasurement
        fields = "__all__"


class HistoricalMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalMeasurement
        fields = "__all__"
