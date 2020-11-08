import time
from utils import Singleton
from config import TIC_TIMEOUT


class Sleep:
    __slots__ = ("tics",)

    def __await__(self):
        return (yield self)

    def __init__(self, tics):
        self.tics = tics


class GameLoop(metaclass=Singleton):
    __slots__ = ('canvas', 'coroutines')

    def __init__(self, coroutines, canvas):
        self.coroutines = []
        self.canvas = canvas
        for cor in coroutines:
            self.add_coroutine(cor)

    def add_coroutine(self, coroutine):
        self.coroutines.append((0, coroutine))

    def start(self):
        while True:
            # let's split coroutines on active and inactive
            active_cors = []
            inactive_cors = []
            for tics, coroutine in self.coroutines:
                if tics <= 0:
                    active_cors.append((tics, coroutine))
                else:
                    inactive_cors.append((tics - 1, coroutine))
            # inactive coroutines
            self.coroutines = inactive_cors

            for _, coroutine in active_cors:
                try:
                    timeout = coroutine.send(None)
                # exhausted coroutine is skipped
                except StopIteration:
                    continue
                self.coroutines.append((timeout.tics, coroutine))

            self.canvas.refresh()
            # 0.1 sec by default
            time.sleep(TIC_TIMEOUT)
