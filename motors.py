from picoed import i2c # type: ignore
from time import sleep
class Motors:
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    BACKWARD = "backward"

    def initialize_motors(self):
        while not i2c.try_lock():
            pass
        try:
            i2c.writeto(0x70, b'\x00\x01')
            i2c.writeto(0x70, b'\xE8\xAA')
            sleep(0.1)  # It is acceptable for initialization to block briefly.
        finally:
            i2c.unlock()

    def move(self, side, direction, speed):
        # Determine the appropriate channels for the motor action.
        if side == Motors.LEFT:
            channel_on, channel_off = (b'\x05', b'\x04') if direction == Motors.FORWARD else (b'\x04', b'\x05')
        elif side == Motors.RIGHT:
            channel_on, channel_off = (b'\x03', b'\x02') if direction == Motors.FORWARD else (b'\x02', b'\x03')
        else:
            return

        while not i2c.try_lock():
            pass
        try:
            i2c.writeto(0x70, channel_off + bytes([0]))
            i2c.writeto(0x70, channel_on + bytes([speed]))
        finally:
            i2c.unlock()

    def stop(self):
        # Stop both motors.
        self.move(Motors.LEFT, Motors.FORWARD, 0)
        self.move(Motors.RIGHT, Motors.FORWARD, 0)
