from django.urls import path
from . import views

urlpatterns = [
    path(
        "historical/type/<str:measurement_type>/",
        views.HistoricalMeasurementsListView.as_view(),
        name="historical_measurements_list",
    ),
    path(
        "historical/<int:pk>/",
        views.HistoricalMeasurementDetailView.as_view(),
        name="historical_measurement_detail",
    ),
    path(
        "fields-dictionary/",
        views.FieldsDictionaryView.as_view(),
        name="fields-dictionary",
    ),
    path(
        "control/led/<str:led_number>/",
        views.LEDControlAPIView.as_view(),
        name="led-control",
    ),
    path("control/gate/", views.GateControlAPIView.as_view(), name="gate-control"),
    path(
        "control/door-servo/",
        views.DoorServoControlAPIView.as_view(),
        name="door-servo-control",
    ),
    path(
        "control/fan/<str:fan_number>/",
        views.FanControlAPIView.as_view(),
        name="fan-control",
    ),
    path(
        "control/servo-vertical/",
        views.ServoVerticalControlAPIView.as_view(),
        name="servo-vertical-control",
    ),
    path(
        "control/servo-horizontal/",
        views.ServoHorizontalControlAPIView.as_view(),
        name="servo-horizontal-control",
    ),
]
