class Navigation:
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    FINISH = "finish"

    def __init__(self, turns=None):
        self.turns = turns or []
        self.current_index = 0
        # This field can be used to remember the last decision when the state machine is busy.
        self.last_decision = Navigation.FORWARD

    def decide_turn(self):
        if self.current_index >= len(self.turns):
            return Navigation.FINISH
        direction = self.turns[self.current_index]
        self.current_index += 1
        return direction
