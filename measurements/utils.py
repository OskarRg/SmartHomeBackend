MQTT_BROKER = "localhost"
MQTT_PORT = 1883


class RGBLedValues:
    def __init__(self, led_number: int, red: int, green: int, blue: int):
        self.led_number = led_number
        self.red = red
        self.green = green
        self.blue = blue

    def to_dict(self):
        return {
            "red": self.red,
            "green": self.green,
            "blue": self.blue,
        }


class CurrentMeasurement:
    def __init__(self, measurement_type, value, date):
        self.measurement_type = measurement_type
        self.value = value
        self.date = date

    MEASUREMENT_TYPES = [
        ("T", "Temperature"),
        ("H", "Humidity"),
        ("P", "Pressure"),
        ("G", "Gas"),
    ]


FIELDS_DICTIONARY: dict[str, dict[str, str | float | RGBLedValues]] = {
    "control": {
        "fan_1_control_status": None,
        "fan_2_control_status": None,
        "is_solar_in_safe_position": None,
        "gate_control": {
            "open": None,
            "close": None,
            "in_progress": None,
            "stopped": None,
        },
        "lock_status": None,
        "door_servo_control": {
            "open": None,
            "close": None,
            "in_progress": None,
            "stopped": None,
        },
    },
    "security": {
        "tilt_sensor_status": {"value": None, "alarm_on": False},
        "pir_sensor_1_status": {"value": None, "alarm_on": False},
        "pir_sensor_2_status": {"value": None, "alarm_on": False},
        "radiation_sensitive_status": {"value": None, "alarm_on": False},
        "buzzer_control_status": None,
        "flame_sensor_status": {"value": None, "alarm_on": False},
        # "rfid_data": "",  # TODO This field will need to reset after each read - (in view after reading)
        "current_pin": "",
    },
    "energy": {
        "leds": {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,
        },
        "energy_consumption": {
            "current_data": None,
            "supply_data": None,  # This might not be right or not work
            "bus_data": None,  # This might not be right or not work
            "power_data": None,
        },
        "energy_production": {
            "current_data": None,
            "supply_data": None,  # This might not be right or not work
            "bus_data": None,  # This might not be right or not work
            "power_data": None,
        },
        "intensity_sensor_data": None,
    },
    "environment": {
        "temperature_data": None,
        "humidity_data": None,
        "pressure_data": None,
        "light_intensity_data": None,  # I don't know what will actually be here, ask someone who is in charge of this
        "gas_data": None,  # I don't know what will actually be here, ask someone who is in charge of this
    },
    "settings": {
        "alarm_time": 30,  # in seconds
        "light_sensor_sensitivity": 50,  # in ???, ask someone who is in charge of this
    },
}


TOPIC_TO_FIELD_MAP = {
    "energy/intensity_sensor/data": ["energy", "intensity_sensor_data"],
    "energy/energy_consumption/current/data": ["energy", "current_data"],
    "energy/energy_consumption/power/data": ["energy", "power_data"],
    "energy/energy_consumption/voltage/supply/data": ["energy", "supply_data"],
    "energy/energy_consumption/voltage/bus/data": ["energy", "bus_data"],
    "energy/LED/1/data": ["energy", "leds", "1"],
    "energy/LED/2/data": ["energy", "leds", "2"],
    "energy/LED/3/data": ["energy", "leds", "3"],
    "energy/LED/4/data": ["energy", "leds", "4"],
    "energy/LED/5/data": ["energy", "leds", "5"],
    "energy/LED/6/data": ["energy", "leds", "6"],
    "security/RFID/data": ["security", "rfid_data"],
    "security/pinpad/data": ["security", "pinpad_data"],
    "security/buzzer/status": ["security", "buzzer_control_status"],
    "security/flame_sensor/status": ["security", "flame_sensor_status"],
    "security/PIR/1/status": ["security", "pir_sensor_1_status"],
    "security/PIR/2/status": ["security", "pir_sensor_2_status"],
    "security/radiation_sensitive/status": ["security", "radiation_sensitive_status"],
    "security/tilt_sensor/status": ["security", "tilt_sensor_status"],
    "control/fan/1/status": ["control", "fan_1_control_status"],
    "control/fan/2/status": ["control", "fan_2_control_status"],
    "control/solar_tracker/servo_horizontal/control": [
        "control",
        "servo_horizontal_control",
    ],
    "control/solar_tracker/servo_vertical/control": [
        "control",
        "servo_vertical_control",
    ],
    "control/gate/motor/control": ["control", "gate_control"],
    "control/door/lock/status": ["control", "lock_status"],
    "control/door/servo/control": ["control", "door_servo_control"],
    "environment/multi_sensor/temperature/data": ["environment", "temperature_data"],
    "environment/multi_sensor/humidity/data": ["environment", "humidity_data"],
    "environment/multi_sensor/pressure/data": ["environment", "pressure_data"],
    "environment/gas_sensor/data": ["environment", "gas_data"],
}
