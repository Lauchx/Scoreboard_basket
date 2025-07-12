from interfaces.timer import time
class Match_time(time):
    def __init__(self, minutes, seconds):
        self.miuntes = minutes
        self.seconds = seconds
        self.is_in_progress = False