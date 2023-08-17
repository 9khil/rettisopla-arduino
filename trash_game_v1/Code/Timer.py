import time


class Timer:
    def __init__(self, Offset = 0):
        self.Reset(Offset)

    def Reset(self, Offset = 0):
        self.StartTime = time.time() - Offset

    def __repr__(self):
        return str(time.time() - self.StartTime)

    def __ge__(self, Other):
        return time.time() - self.StartTime >= Other

    def __truediv__(self, Other):
        return (time.time() - self.StartTime) / Other