import config
import time
from utils import Singleton


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
        # 0.1 sec by default
        tic = config.TIC_TIMEOUT
        while True:
            # let's split coroutines on active and inactive
            active_cors = []
            arr = []
            for tics, cor in self.coroutines:
                tics -= 1
                if tics <= 0:
                    active_cors.append((tics, cor))
                else:
                    arr.append((tics, cor))
            # inactive coroutines
            self.coroutines = arr

            for _, cor in active_cors:
                try:
                    timeout = cor.send(None)
                # exhausted coroutine is skipped
                except StopIteration:
                    continue
                self.coroutines.append((timeout.tics, cor))

            self.canvas.refresh()
            time.sleep(tic)
