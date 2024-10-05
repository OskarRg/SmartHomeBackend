import django_filters
from django_filters import DateFromToRangeFilter
from .models import CurrentMeasurement, HistoricalMeasurement


class CurrentMeasurementFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = CurrentMeasurement
        fields = ["date", "room", "type"]


class HistoricalMeasurementFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = HistoricalMeasurement
        fields = ["date", "room", "type"]
