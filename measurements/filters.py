import django_filters
from django_filters import DateFromToRangeFilter
from .models import (
    HistoricalMeasurement,
    EnergyProductionMeasurement,
    EnergyConsumptionMeasurement,
)


class HistoricalMeasurementFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = HistoricalMeasurement
        fields = ["date"]


class EnergyConsumptionMeasurementFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = EnergyConsumptionMeasurement
        fields = ["date"]


class EnergyProductionMeasurementFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = EnergyProductionMeasurement
        fields = ["date"]
