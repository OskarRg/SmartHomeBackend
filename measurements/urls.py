from django.urls import path
from . import views

urlpatterns = [
    path(
        "current/",
        views.CurrentMeasurementsListView.as_view(),
        name="current_measurements_list",
    ),
    path(
        "current/<int:pk>/",
        views.CurrentMeasurementDetailView.as_view(),
        name="current_measurement_detail",
    ),
    path(
        "historical/",
        views.HistoricalMeasurementsListView.as_view(),
        name="historical_measurements_list",
    ),
    path(
        "historical/<int:pk>/",
        views.HistoricalMeasurementDetailView.as_view(),
        name="historical_measurement_detail",
    ),
]
