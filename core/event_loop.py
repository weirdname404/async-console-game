import config
import time


class Sleep:
    __slots__ = ("tics",)

    def __await__(self):
        return (yield self)

    def __init__(self, tics):
        self.tics = tics


def start_game_loop(coroutines, canvas):
    # 0.1 sec by default
    tic = config.TIC_TIMEOUT
    sleeping_cors = [(0, cor) for cor in coroutines]

    while True:
        # let's split coroutines on active and unactive
        active_cors = []
        arr = []
        for tics, cor in sleeping_cors:
            tics -= 1
            if tics <= 0:
                active_cors.append((tics, cor))
            else:
                arr.append((tics, cor))

        sleeping_cors = arr

        for _, cor in active_cors:
            try:
                timeout = cor.send(None)
            # exhausted coroutine is skipped
            except StopIteration:
                continue
            sleeping_cors.append((timeout.tics, cor))

        canvas.refresh()
        time.sleep(tic)
