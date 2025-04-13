from neopixel import NeoPixel
from duration import Duration
from board import P0

class Lights:
    """
    Manages the robot's LED lighting system, including indicators and brake lights.
    Controls individual LEDs through the NeoPixel interface.
    """
    INDICATOR_LEFT_FORWARD = 3
    INDICATOR_LEFT_REVERSE = 6
    INDICATOR_RIGHT_FORWARD = 0
    INDICATOR_RIGHT_REVERSE = 5
    BREAK_LEFT = 7
    BREAK_RIGHT = 4
    DURATION_SECONDS = 0.5

    def __init__(self):
        """
        Initialize the lighting system with NeoPixel control.
        """
        self.neopixel = NeoPixel(P0, 8)
        self.left_forward = Light(Lights.INDICATOR_LEFT_FORWARD, self.neopixel, Light.COLOR_ORANGE)
        self.left_reverse = Light(Lights.INDICATOR_LEFT_REVERSE, self.neopixel, Light.COLOR_ORANGE)
        self.right_forward = Light(Lights.INDICATOR_RIGHT_FORWARD, self.neopixel, Light.COLOR_ORANGE)
        self.right_reverse = Light(Lights.INDICATOR_RIGHT_REVERSE, self.neopixel, Light.COLOR_ORANGE)
        self.break_left = Light(Lights.BREAK_LEFT, self.neopixel, Light.COLOR_RED)
        self.break_right = Light(Lights.BREAK_RIGHT, self.neopixel, Light.COLOR_RED)
        self.duration = None
        self.mode = None
        self.lights_on = False

    def __toggle_indicators(self, left_on, right_on):
        """
        Toggle the state of the indicator lights.
        
        Args:
            left_on: Whether to turn on the left indicators
            right_on: Whether to turn on the right indicators
        """
        if left_on:
            self.left_forward.on()
            self.left_reverse.on()
        else:
            self.left_forward.off()
            self.left_reverse.off()

        if right_on:
            self.right_forward.on()
            self.right_reverse.on()
        else:
            self.right_forward.off()
            self.right_reverse.off()

    def indicate_left(self):
        """
        Activate the left turn indicators with blinking behavior.
        """
        self.mode = 'left'
        if self.duration is None or self.duration.done():
            self.duration = Duration(Lights.DURATION_SECONDS)
            self.lights_on = not self.lights_on
            self.__toggle_indicators(self.lights_on, False)

    def indicate_right(self):
        """
        Activate the right turn indicators with blinking behavior.
        """
        self.mode = 'right'
        if self.duration is None or self.duration.done():
            self.duration = Duration(Lights.DURATION_SECONDS)
            self.lights_on = not self.lights_on
            self.__toggle_indicators(False, self.lights_on)

    def turn_off(self):
        """
        Turn off all indicator lights.
        """
        self.mode = None
        self.lights_on = False
        self.__toggle_indicators(False, False)

    def blink_all(self):
        """
        Blink all indicator lights simultaneously.
        """
        self.mode = 'all'
        if self.duration is None or self.duration.done():
            self.duration = Duration(Lights.DURATION_SECONDS)
            self.lights_on = not self.lights_on
            self.__toggle_indicators(self.lights_on, self.lights_on)

    def break_on(self):
        """
        Turn on the brake lights.
        """
        self.break_left.on()
        self.break_right.on()

    def break_off(self):
        """
        Turn off the brake lights.
        """
        self.break_left.off()
        self.break_right.off()

class Light:
    """
    Represents a single LED with position and color control.
    """
    COLOR_ORANGE = (255, 100, 0)
    COLOR_OFF = (0, 0, 0)
    COLOR_RED = (100, 0, 0)

    def __init__(self, position, neo, color):
        """
        Initialize a single LED.
        
        Args:
            position: LED position in the NeoPixel array
            neo: NeoPixel control interface
            color: Default color for the LED
        """
        self.position = position
        self.neo = neo
        self.color = color

    def on(self):
        """
        Turn on the LED with its configured color.
        """
        self.neo[self.position] = self.color
        self.neo.write()

    def off(self):
        """
        Turn off the LED.
        """
        self.neo[self.position] = Light.COLOR_OFF
        self.neo.write()
