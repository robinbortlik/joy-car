from state import State
from duration import Duration
from control_unit import ControlUnit
from navigation import Navigation

class Robot:
    STATE_DRIVING = "D"
    STATE_MOVE_TO_INTERSECTION = "MTI"
    STATE_RESOLVE_INTERSECTION = "RI"
    STATE_TURN_LEFT = "TL"
    STATE_TURN_RIGHT = "TR"
    STATE_FINISH = "F"
    STATE_BREAK = "B"
    STATE_ERROR = "E"


    def __init__(self, control_unit, navigation):
        self.control_unit = control_unit
        self.navigation = navigation
        self.robot_state = State(Robot.STATE_DRIVING, display_state=True)
        self.no_line_duration = None

    def start(self):
        self.control_unit.lights.turn_off()
        self.control_unit.initialize()

    def drive(self):
        obstacle = self.control_unit.is_obstacle()

        # Update the state machine
        self.robot_state.update()

        if self.robot_state.current_state == Robot.STATE_FINISH or self.robot_state.current_state == Robot.STATE_ERROR:
            self.control_unit.execute_movement(ControlUnit.COMMAND_FINISH)
            return

        if self.robot_state.current_state == Robot.STATE_BREAK:
            self.control_unit.execute_movement(ControlUnit.COMMAND_BREAK)
            return

        if self.robot_state.current_state == Robot.STATE_MOVE_TO_INTERSECTION:
            self.robot_state.duration = Duration(0.4)
            self.robot_state.set_state(Robot.STATE_DRIVING, condition=lambda: self.robot_state.duration.done(), next_state=Robot.STATE_RESOLVE_INTERSECTION)
            return

        if self.robot_state.current_state == Robot.STATE_RESOLVE_INTERSECTION:
            turn_direction = self.navigation.decide_turn()
            if turn_direction == Navigation.LEFT:
                self.robot_state.set_state(Robot.STATE_TURN_LEFT, condition=lambda: self.control_unit.line_sensors.is_left(), next_state=Robot.STATE_DRIVING)

            elif turn_direction == Navigation.RIGHT:
                self.robot_state.set_state(Robot.STATE_TURN_RIGHT, condition=lambda: self.control_unit.line_sensors.is_right(), next_state=Robot.STATE_DRIVING)

            elif turn_direction == Navigation.FORWARD:
                self.robot_state.set_state(Robot.STATE_DRIVING)
            elif turn_direction == Navigation.FINISH:
                self.robot_state.set_state(Robot.STATE_FINISH, condition=lambda: False)
            return

        if self.robot_state.current_state == Robot.STATE_TURN_LEFT:
            self.control_unit.execute_movement(ControlUnit.COMMAND_LEFT)
            return

        if self.robot_state.current_state == Robot.STATE_TURN_RIGHT:
            self.control_unit.execute_movement(ControlUnit.COMMAND_RIGHT)
            return

        if self.control_unit.line_sensors.is_intersection() and self.robot_state.current_state == Robot.STATE_DRIVING:
            self.robot_state.duration = Duration(0.5)
            self.robot_state.set_state(Robot.STATE_BREAK, condition=lambda: self.robot_state.duration.done(), next_state=Robot.STATE_MOVE_TO_INTERSECTION)
            return


        if self.control_unit.line_sensors.no_line():
            if self.no_line_duration is None:
                self.no_line_duration = Duration(3.0)
            elif self.no_line_duration.done():
                self.robot_state.set_state(Robot.STATE_ERROR, condition=lambda: False)
            return
        else:
            self.no_line_duration = None

        if self.robot_state.current_state == Robot.STATE_DRIVING:
            self.control_unit.execute_movement(ControlUnit.COMMAND_FORWARD)
            return


    def stop(self):
        self.control_unit.stop()
