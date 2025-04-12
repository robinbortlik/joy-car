from time import monotonic_ns

class Duration:
    """
    Manages a duration with nanosecond precision.
    """
    def __init__(self, duration_secs=0):
        self.start_time = monotonic_ns()
        self.duration_ns = int(duration_secs * 1_000_000_000)  # Convert seconds to nanoseconds

    def done(self):
        """
        Returns True if the duration has elapsed, False otherwise.
        """
        return self.duration_ns > 0 and (monotonic_ns() - self.start_time >= self.duration_ns)
