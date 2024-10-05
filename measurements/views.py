from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import CurrentMeasurement, HistoricalMeasurement
from .serializers import CurrentMeasurementSerializer, HistoricalMeasurementSerializer


class CurrentMeasurementsListView(generics.ListAPIView):
    serializer_class = CurrentMeasurementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["room", "type"]
    ordering_fields = ["date"]

    def get_queryset(self):

        return CurrentMeasurement.objects.filter()


class HistoricalMeasurementsListView(generics.ListAPIView):
    serializer_class = HistoricalMeasurementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["room", "type"]
    ordering_fields = ["date"]

    def get_queryset(self):
        measurement_type = self.kwargs["measurement_type"]

        return HistoricalMeasurement.objects.filter(type=measurement_type)


class HistoricalMeasurementDetailView(generics.RetrieveDestroyAPIView):
    queryset = HistoricalMeasurement.objects.all()
    serializer_class = HistoricalMeasurementSerializer


class CurrentMeasurementDetailView(generics.RetrieveDestroyAPIView):
    queryset = CurrentMeasurement.objects.all()
    serializer_class = CurrentMeasurementSerializer
