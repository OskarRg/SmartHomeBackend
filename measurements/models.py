from django.db import models


class CurrentMeasurement(models.Model):
    MEASUREMENT_TYPES = [
        ("T", "Temperature"),
        ("H", "Humidity"),
        ("P", "Pressure"),
        ("G", "Gas"),
    ]

    type = models.CharField(max_length=10, choices=MEASUREMENT_TYPES)
    value = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"CurrentMeasurement in {self.room.name}"


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
    # date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HistoricalMeasurement in {self.room.name} on {self.date}"


class RGBLedValues(models.Model):
    led_number = models.IntegerField()
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()

    def __str__(self):
        return f"LED {self.led_number}: ({self.red}, {self.green}, {self.blue})"


class Control(models.Model):
    fan_control_status = models.BooleanField()
    servo_vertical_control = models.IntegerField()
    servo_horizontal_control = models.IntegerField()
    gate_control = models.IntegerField()
    lock_status = models.BooleanField()
    door_servo_control = models.IntegerField()


class Security(models.Model):
    tilt_sensor_status = models.BooleanField()
    pir_sensor_1_status = models.BooleanField()
    pir_sensor_2_status = models.BooleanField()
    radiation_sensitive_status = models.BooleanField()
    buzzer_control_status = models.BooleanField()
    flame_sensor_status = models.BooleanField()
    rfid_data = models.TextField()
    pin_pad_data = models.TextField()


class Energy(models.Model):
    current_data = models.FloatField()
    voltage_supply_data = models.FloatField()
    voltage_bus_data = models.FloatField()
    power_data = models.FloatField()
    leds = models.ManyToManyField(RGBLedValues)
    intensity_sensor_data = models.FloatField()


class Environment(models.Model):
    current_measurements = models.OneToOneField(CurrentMeasurement, on_delete=models.CASCADE)
    historical_measurements = models.ManyToManyField(HistoricalMeasurement)


class Home(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    control = models.OneToOneField(Control, on_delete=models.CASCADE)
    security = models.OneToOneField(Security, on_delete=models.CASCADE)
    energy = models.OneToOneField(Energy, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RFIDCard(models.Model):
    card_id = models.CharField(max_length=100, unique=True)
    owner = models.CharField(max_length=100)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_id

