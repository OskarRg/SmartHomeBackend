from django.contrib import admin
from .models import RFIDCard, HistoricalMeasurement


admin.site.register(RFIDCard)
admin.site.register(HistoricalMeasurement)
