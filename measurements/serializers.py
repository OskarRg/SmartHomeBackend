from rest_framework import serializers
from .models import CurrentMeasurement, HistoricalMeasurement


class CurrentMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentMeasurement
        fields = "__all__"


class HistoricalMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalMeasurement
        fields = "__all__"
