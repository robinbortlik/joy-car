from board import P2
from analogio import AnalogIn

class Battery:
    MIN_VOLTAGE = 5.5

    def __init__(self):
        self.pin = PinADC(P2)

    def ok(self):
        return self.get_voltage() > Battery.MIN_VOLTAGE

    def get_voltage(self):
        # vrať velikost napájecího napětí
        return self.pin.get_supply_voltage()


class PinADC:
    def __init__(self, pin):
        self.pinName = pin
        self.pin = AnalogIn(self.pinName)

    def read_analog(self):
        # print(self.pin.value)
        return self.pin.value // 64

    def get_supply_voltage(self):
        # vrať velikost napájecího napětí
        return 0.00898 * self.read_analog()
