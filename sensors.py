from machine import ADC, Pin


class Sensors(object):
    SAMPLES = 20

    def __init__(self):
        self.temperature_sensor = ADC(4)
        self.battery_sensor = ADC(0)
        self.smps_pin = Pin(23, Pin.OUT)
        self.smps_pin.value(1)

    def read_temperature(self):
        samples = []
        for i in range(self.SAMPLES):
            samples.append(self.temperature_sensor.read_u16())

        reading = sum(samples) / len(samples)
        reading *= 3.3 / 65535
        temperature = 27 - (reading - 0.706) / 0.001721
        return round(temperature, 1)

    def read_battery(self):
        samples = []
        for i in range(self.SAMPLES):
            samples.append(self.battery_sensor.read_u16())

        reading = sum(samples) / len(samples)
        reading *= 6.6 / 65535
        percentage = (reading - 3.3) / 0.8
        percentage = round(100 * max(min(percentage, 1.0), 0.0))
        if percentage >= 66:
            icon = "https://cdn-icons-png.flaticon.com/512/3103/3103446.png"
        elif percentage >= 33:
            icon = "https://cdn-icons-png.flaticon.com/512/3103/3103529.png"
        else:
            icon = "https://cdn-icons-png.flaticon.com/512/3103/3103520.png"
        return (percentage, icon)
