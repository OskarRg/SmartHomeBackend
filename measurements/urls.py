from django.urls import path
from . import views


# TODO Sort the urls in alphabetical order
urlpatterns = [
    path(
        "historical/type/<str:measurement_type>/",
        views.HistoricalMeasurementsListView.as_view(),
        name="historical_measurements_list",
    ),
    path(
        "consumption/type/<str:measurement_type>/",
        views.EnergyConsumptionListView.as_view(),
        name="consumption_measurements_list",
    ),
    path(
        "production/type/<str:measurement_type>/",
        views.EnergyProductionListView.as_view(),
        name="production_measurements_list",
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
        "control/solar-position/",
        views.SolarPanelPositionAPIView.as_view(),
        name="solar-control",
    ),
    path(
        "security/buzzer/",
        views.TurnOffBuzzer.as_view(),
        name="buzzer-control",
    ),
    path(
        "settings/light-sensitivity/",
        views.LightSensitivityChangeAPIView.as_view(),
        name="light-setting",
    ),
    path(
        "security/change-current-pin/",
        views.PinChangeAPIView.as_view(),
        name="change-current-pin",
    ),
    path(
        "settings/set-alarm/",
        views.SetAlarmAPIView.as_view(),
        name="set-alarm",
    ),
    path(
        "settings/set-armed-alarm/",
        views.ArmedAlarm.as_view(),
        name="set-armed-alarm",
    ),
    path(
        "security/set-rfid/",
        views.AddRFIDAPIView.as_view(),
        name="set-rfid",
    ),
]
