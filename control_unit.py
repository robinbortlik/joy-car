from motors import Motors
class ControlUnit:
    """
    Controls the robot's movement and behavior based on sensor inputs and commands.
    Manages motor control, line following, and obstacle avoidance.
    """
    COMMAND_FORWARD = "forward"
    COMMAND_LEFT = "left"
    COMMAND_RIGHT = "right"
    COMMAND_FINISH = "finish"
    COMMAND_BREAK = "break"
    SPEED_MULTIPLIER = 1

    def __init__(self, line_sensors, motors, obstacle_sensor, lights):
        """
        Initialize the control unit with required sensors and actuators.

        Args:
            line_sensors: Line sensor interface
            motors: Motor control interface
            obstacle_sensor: Obstacle detection interface
            lights: Light control interface
        """
        self.line_sensors = line_sensors
        self.motors = motors
        self.obstacle_sensor = obstacle_sensor
        self.lights = lights

    def initialize(self):
        """
        Initialize the motor control system.
        """
        self.motors.initialize_motors()

    def is_obstacle(self):
        """
        Check if an obstacle is detected.

        Returns:
            bool: True if obstacle is detected, False otherwise
        """
        return False

    def execute_movement(self, command):
        """
        Execute a movement command based on the given command.

        Args:
            command: The movement command to execute
        """
        if command != ControlUnit.COMMAND_BREAK:
            self.lights.break_off()

        if command == ControlUnit.COMMAND_FORWARD:
            self.__move_forward()
        elif command == ControlUnit.COMMAND_LEFT:
            self.__turn_left()
        elif command == ControlUnit.COMMAND_RIGHT:
            self.__turn_right()
        elif command == ControlUnit.COMMAND_FINISH:
            self.stop()
            self.lights.blink_all()
        elif command == ControlUnit.COMMAND_BREAK:
            self.lights.break_on()
            self.stop()

    def stop(self):
        """
        Stop all motor movement.
        """
        self.motors.stop()

    def __turn_left(self):
        """
        Execute a left turn maneuver.
        """
        self.lights.indicate_left()
        self.motors.move(Motors.LEFT, Motors.BACKWARD, self.speed(110))
        self.motors.move(Motors.RIGHT, Motors.FORWARD, self.speed(110))

    def __turn_right(self):
        """
        Execute a right turn maneuver.
        """
        self.lights.indicate_right()
        self.motors.move(Motors.LEFT, Motors.FORWARD, self.speed(110))
        self.motors.move(Motors.RIGHT, Motors.BACKWARD, self.speed(110))

    def __move_forward(self):
        """
        Execute forward movement with line following behavior.
        Adjusts motor speeds based on line sensor readings.
        """
        self.lights.turn_off()
        line_sensors = self.line_sensors.get_state()
        if line_sensors["left"]:
            self.motors.move(Motors.LEFT, Motors.FORWARD, self.speed(30))
            self.motors.move(Motors.RIGHT, Motors.FORWARD, self.speed(90))
        elif line_sensors["right"]:
            self.motors.move(Motors.LEFT, Motors.FORWARD, self.speed(90))
            self.motors.move(Motors.RIGHT, Motors.FORWARD, self.speed(30))
        elif line_sensors["center"]:
            self.motors.move(Motors.LEFT, Motors.FORWARD, self.speed(90))
            self.motors.move(Motors.RIGHT, Motors.FORWARD, self.speed(90))

    def speed(self, speed):
        return int(speed * ControlUnit.SPEED_MULTIPLIER)
