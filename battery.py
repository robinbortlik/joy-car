from board import P2
from analogio import AnalogIn

class Battery:
    """
    Manages battery voltage monitoring and status checking.
    """
    MIN_VOLTAGE = 5.5

    def __init__(self):
        self.pin = PinADC(P2)

    def ok(self):
        """
        Returns True if the battery voltage is above the minimum threshold.
        """
        return self.get_voltage() > Battery.MIN_VOLTAGE

    def get_voltage(self):
        """
        Returns the current supply voltage in volts.
        """
        return self.pin.get_supply_voltage()


class PinADC:
    """
    Handles analog-to-digital conversion for voltage measurement.
    """
    def __init__(self, pin):
        self.pinName = pin
        self.pin = AnalogIn(self.pinName)

    def read_analog(self):
        """
        Reads the raw analog value from the pin.
        """
        return self.pin.value // 64

    def get_supply_voltage(self):
        """
        Converts the analog reading to supply voltage in volts.
        """
        return 0.00898 * self.read_analog()
