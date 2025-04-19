from state import State
from duration import Duration
from control_unit import ControlUnit
from navigation import Navigation

class Robot:
    """
    Main robot control class that implements the state machine for autonomous navigation.
    Manages the robot's behavior through different states and handles transitions between them.
    """
    # State constants representing different robot behaviors
    STATE_DRIVING = "D"  # Normal line following state
    STATE_MOVE_TO_INTERSECTION = "MTI"  # Moving through an intersection
    STATE_RESOLVE_INTERSECTION = "RI"  # Deciding which way to turn at intersection
    STATE_TURN_LEFT = "TL"  # Executing left turn
    STATE_TURN_RIGHT = "TR"  # Executing right turn
    STATE_FINISH = "F"  # Mission complete state
    STATE_BREAK = "B"  # Temporary stop state
    STATE_ERROR = "E"  # Error state (e.g., lost line)

    def __init__(self, control_unit, navigation):
        """
        Initialize the robot with control unit and navigation system.

        Args:
            control_unit: ControlUnit instance for motor and sensor control
            navigation: Navigation instance for route planning
        """
        self.control_unit = control_unit
        self.navigation = navigation
        self.robot_state = State(Robot.STATE_DRIVING, display_state=True)
        self.no_line_duration = None

    def start(self):
        """
        Initialize the robot's systems and prepare for operation.
        Turns off all lights and initializes the control unit.
        """
        self.control_unit.lights.turn_off()
        self.control_unit.initialize()

    def drive(self):
        """
        Main control loop that implements the robot's state machine.
        This function is called repeatedly to update the robot's state and behavior.

        The state machine handles:
        1. Obstacle detection (not implemented yet)
        2. Line following
        3. Intersection detection and handling
        4. Turn execution
        5. Error conditions (e.g., lost line)

        State transitions:
        - DRIVING -> BREAK -> MOVE_TO_INTERSECTION -> RESOLVE_INTERSECTION -> (TURN_LEFT/TURN_RIGHT/DRIVING)
        - DRIVING -> ERROR (when line is lost for too long)
        - Any state -> FINISH (when mission is complete)

        Each state has specific conditions for transitions and associated actions.
        """
        # Check for obstacles
        obstacle = self.control_unit.is_obstacle()

        # Update the state machine
        self.robot_state.update()

        # Handle terminal states (FINISH and ERROR)
        if self.robot_state.current_state == Robot.STATE_FINISH or self.robot_state.current_state == Robot.STATE_ERROR:
            self.control_unit.execute_movement(ControlUnit.COMMAND_FINISH)
            return

        # Handle break state (temporary stop)
        if self.robot_state.current_state == Robot.STATE_BREAK:
            self.control_unit.execute_movement(ControlUnit.COMMAND_BREAK)
            return

        # Handle moving through intersection
        if self.robot_state.current_state == Robot.STATE_MOVE_TO_INTERSECTION:
            self.robot_state.duration = Duration(0.4)
            self.robot_state.set_state(Robot.STATE_DRIVING, condition=lambda: self.robot_state.duration.done(), next_state=Robot.STATE_RESOLVE_INTERSECTION)
            return

        # Handle intersection resolution (deciding which way to turn)
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

        # Handle left turn execution
        if self.robot_state.current_state == Robot.STATE_TURN_LEFT:
            self.control_unit.execute_movement(ControlUnit.COMMAND_LEFT)
            return

        # Handle right turn execution
        if self.robot_state.current_state == Robot.STATE_TURN_RIGHT:
            self.control_unit.execute_movement(ControlUnit.COMMAND_RIGHT)
            return

        # Detect intersection and initiate turn sequence
        if self.control_unit.line_sensors.is_intersection() and self.robot_state.current_state == Robot.STATE_DRIVING:
            self.robot_state.duration = Duration(0.5)
            self.robot_state.set_state(Robot.STATE_BREAK, condition=lambda: self.robot_state.duration.done(), next_state=Robot.STATE_MOVE_TO_INTERSECTION)
            return

        # Handle lost line condition
        if self.control_unit.line_sensors.no_line():
            if self.no_line_duration is None:
                self.no_line_duration = Duration(5.0)
            elif self.no_line_duration.done():
                self.robot_state.set_state(Robot.STATE_ERROR, condition=lambda: False)
            return
        else:
            self.no_line_duration = None

        # Normal line following behavior
        if self.robot_state.current_state == Robot.STATE_DRIVING:
            self.control_unit.execute_movement(ControlUnit.COMMAND_FORWARD)
            return

    def stop(self):
        """
        Stop all robot movement and halt the control systems.
        """
        self.control_unit.stop()
