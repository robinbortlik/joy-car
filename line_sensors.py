from picoed import i2c # type: ignore

class LineSensors:
    def read(self):
        while not i2c.try_lock():
            pass
        try:
            buffer = bytearray(1)
            i2c.readfrom_into(0x38, buffer, start=0, end=1)
            data_bit_string = self.byte_to_bits(buffer)
            # Return three booleans corresponding to the left, center, and right sensors.
            return bool(int(data_bit_string[7])), bool(int(data_bit_string[6])), bool(int(data_bit_string[5]))
        finally:
            i2c.unlock()

    def byte_to_bits(self, buffer):
        data_int = int.from_bytes(buffer, "big")
        data_bit_string = bin(data_int)
        return data_bit_string

    def get_state(self):
        left, center, right = self.read()
        return {
            "left": left,
            "center": center,
            "right": right,
            "is_intersection": sum([left, center, right]) >= 2,
        }

    def is_intersection(self):
        return self.get_state()["is_intersection"]

    def is_left(self):
        return self.get_state()["left"]

    def is_center(self):
        return self.get_state()["center"]

    def is_right(self):
        return self.get_state()["right"]

    def no_line(self):
        return not self.is_left() and not self.is_center() and not self.is_right()
