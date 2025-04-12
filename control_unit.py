from motors import Motors
class ControlUnit:
    COMMAND_FORWARD = "forward"
    COMMAND_LEFT = "left"
    COMMAND_RIGHT = "right"
    COMMAND_FINISH = "finish"
    COMMAND_BREAK = "break"
    SPEED_MULTIPLIER = 1


    def __init__(self, line_sensors, motors, obstacle_sensor, lights):
        self.line_sensors = line_sensors
        self.motors = motors
        self.obstacle_sensor = obstacle_sensor
        self.lights = lights

    def initialize(self):
        self.motors.initialize_motors()


    def is_obstacle(self):
        return False


    def execute_movement(self, command):
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
        self.motors.stop()

    def __turn_left(self):
        self.lights.indicate_left()
        self.motors.move(Motors.LEFT, Motors.BACKWARD, self.speed(90))
        self.motors.move(Motors.RIGHT, Motors.FORWARD, self.speed(90))


    def __turn_right(self):
        self.lights.indicate_right()
        self.motors.move(Motors.LEFT, Motors.FORWARD, self.speed(90))
        self.motors.move(Motors.RIGHT, Motors.BACKWARD, self.speed(90))


    def __move_forward(self):
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
