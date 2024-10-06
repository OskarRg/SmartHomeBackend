import django_filters
from django_filters import DateFromToRangeFilter
from .models import HistoricalMeasurement


class HistoricalMeasurementFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = HistoricalMeasurement
        fields = ["date"]
