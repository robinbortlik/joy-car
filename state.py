from picoed import display

class State:
    """
    Manages the robot's current state with a lambda function to determine state persistence.
    """
    def __init__(self, default_state="driving", display_state=None):
        self.current_state = default_state
        self.default_state = default_state
        self.state_condition = lambda: True  # Default condition that always returns True
        self.next_state = None
        self.display_state = display_state

    def set_state(self, new_state, condition=lambda: True, next_state=None):
        if self.current_state != new_state:
            print(f"State changed from {self.current_state} to {new_state}")
        """
        Set a new state with a condition lambda function.
        The state will persist until the condition returns True.
        """
        self.current_state = new_state
        self.state_condition = condition
        self.next_state = next_state
        if self.display_state:
            display.show(self.current_state)


    def update(self):
        """
        Check if the state condition is met, and if so, revert to 'driving'.
        """
        if self.state_condition():
            self.set_state(self.next_state or self.default_state)
