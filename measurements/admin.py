from django.contrib import admin
from .models import Home, RFIDCard, CurrentMeasurement, HistoricalMeasurement

admin.site.register(Home)
admin.site.register(RFIDCard)
admin.site.register(CurrentMeasurement)
admin.site.register(HistoricalMeasurement)
