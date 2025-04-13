from picoed import i2c # type: ignore

class LineSensors:
    """
    Manages the line following sensors and provides methods to read and interpret their states.
    Handles I2C communication with the sensor hardware.
    """
    def read(self):
        """
        Read the raw sensor values from the I2C device.
        
        Returns:
            tuple: Three boolean values representing left, center, and right sensor states
        """
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
        """
        Convert a byte buffer to a binary string representation.
        
        Args:
            buffer: Byte buffer to convert
            
        Returns:
            str: Binary string representation of the byte
        """
        data_int = int.from_bytes(buffer, "big")
        data_bit_string = bin(data_int)
        return data_bit_string

    def get_state(self):
        """
        Get the current state of all line sensors.
        
        Returns:
            dict: Dictionary containing sensor states and intersection detection
        """
        left, center, right = self.read()
        return {
            "left": left,
            "center": center,
            "right": right,
            "is_intersection": sum([left, center, right]) >= 2,
        }

    def is_intersection(self):
        """
        Check if the robot is at an intersection.
        
        Returns:
            bool: True if at least two sensors detect a line
        """
        return self.get_state()["is_intersection"]

    def is_left(self):
        """
        Check if the left sensor detects a line.
        
        Returns:
            bool: True if left sensor detects a line
        """
        return self.get_state()["left"]

    def is_center(self):
        """
        Check if the center sensor detects a line.
        
        Returns:
            bool: True if center sensor detects a line
        """
        return self.get_state()["center"]

    def is_right(self):
        """
        Check if the right sensor detects a line.
        
        Returns:
            bool: True if right sensor detects a line
        """
        return self.get_state()["right"]

    def no_line(self):
        """
        Check if no sensors detect a line.
        
        Returns:
            bool: True if no sensors detect a line
        """
        return not self.is_left() and not self.is_center() and not self.is_right()
