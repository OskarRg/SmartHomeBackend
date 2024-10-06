from django.apps import AppConfig


class MeasurementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "measurements"

    def ready(self):
        from .mqtt_topic_input_handler import start_mqtt_client

        # Uruchom klienta MQTT po uruchomieniu aplikacji Django
        start_mqtt_client()
