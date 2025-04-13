class Navigation:
    """
    Manages the robot's navigation through a predefined sequence of turns.
    Maintains the current state of navigation and determines the next movement.
    """
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    FINISH = "finish"

    def __init__(self, turns=None):
        """
        Initialize the navigation system with a sequence of turns.
        
        Args:
            turns: List of turn directions to execute
        """
        self.turns = turns or []
        self.current_index = 0
        # This field can be used to remember the last decision when the state machine is busy.
        self.last_decision = Navigation.FORWARD

    def decide_turn(self):
        """
        Determine the next turn direction based on the predefined sequence.
        
        Returns:
            str: The next turn direction or FINISH if sequence is complete
        """
        if self.current_index >= len(self.turns):
            return Navigation.FINISH
        direction = self.turns[self.current_index]
        self.current_index += 1
        return direction
