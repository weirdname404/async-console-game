import config
import time


class Sleep:
    __slots__ = ("tics",)

    def __await__(self):
        return (yield self)

    def __init__(self, tics):
        self.tics = tics


async def static_sleep(amount_of_tics):
    for _ in range(amount_of_tics):
        await Sleep(0)


def game_event_loop(
    static_coroutines, dynamic_coroutines, spaceship_coroutine, canvas
):
    # 0.1 sec by default
    tic = config.TIC_TIMEOUT
    sleeping_cors = [(0, cor) for cor in dynamic_coroutines]
    max_y, max_x = canvas.getmaxyx()
    spaceship = spaceship_coroutine(canvas=canvas, x=max_x//2, y=max_y-10)

    while True:
        # static coroutines don't change and don't exhaust
        for cor in static_coroutines:
            cor.send(None)

        # dynamic coroutines can exhaust and can change
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

        # spaceship contoller
        spaceship.send(None)

        canvas.refresh()
        time.sleep(tic)
