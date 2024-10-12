from django.db import models


class HistoricalMeasurement(models.Model):
    MEASUREMENT_TYPES = [
        ("T", "Temperature"),
        ("H", "Humidity"),
        ("P", "Pressure"),
        ("G", "Gas"),
    ]

    type = models.CharField(max_length=10, choices=MEASUREMENT_TYPES)
    value = models.FloatField()
    date = models.DateTimeField()


class EnergyConsumptionMeasurement(models.Model):
    MEASUREMENT_TYPES = [
        ("B", "Bus"),
        ("C", "Current"),
        ("P", "Power"),
        ("S", "Supply"),
    ]

    type = models.CharField(max_length=10, choices=MEASUREMENT_TYPES)
    value = models.FloatField()
    date = models.DateTimeField()


class EnergyProductionMeasurement(models.Model):
    MEASUREMENT_TYPES = [
        ("B", "Bus"),
        ("C", "Current"),
        ("P", "Power"),
        ("S", "Supply"),
    ]

    type = models.CharField(max_length=10, choices=MEASUREMENT_TYPES)
    value = models.FloatField()
    date = models.DateTimeField()


class RFIDCard(models.Model):
    owner = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.owner}"
