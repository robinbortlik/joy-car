from picoed import button_a, button_b, display # type: ignore
from time import sleep
from robot import Robot
from line_sensors import LineSensors
from motors import Motors
from obstacle_sensor import ObstacleSensor
from navigation import Navigation
from control_unit import ControlUnit
from lights import Lights
import traceback  # Add this import for MicroPython error handling
from battery import Battery

if __name__ == "__main__":

    navigation = Navigation(turns=[
        Navigation.FORWARD,
        Navigation.LEFT,
        Navigation.RIGHT,
        Navigation.LEFT,
        Navigation.FORWARD,
        Navigation.LEFT,
        Navigation.FORWARD,
        Navigation.LEFT,
        Navigation.FORWARD,
        Navigation.RIGHT,
        Navigation.LEFT,
        Navigation.LEFT

    ])

    control_unit = ControlUnit(
        LineSensors(),
        Motors(),
        ObstacleSensor(),
        Lights()
    )
    robot = Robot(control_unit, navigation)
    battery = Battery()

    while not battery.ok():
        print("Battery is not ok. Stopping the robot.")
        robot.stop()
        display.show("LOW BATTERY " + str(battery.get_voltage()) + "V")
        sleep(1)

    try:
        robot.start()

        print("Press button A to start the robot.")
        while not button_a.was_pressed():
            sleep(0.1)

        # Main loop – note there is only one sleep call here.
        while not button_b.was_pressed():
            robot.drive()
            sleep(0.02)  # This sleep maintains a fixed update rate.

        robot.stop()
    except Exception as e:
        print("An error occurred. Stopping the robot.")
        print("Error details:")
        traceback.print_exception(e)  # Print full stack trace using MicroPython's method
        robot.stop()
