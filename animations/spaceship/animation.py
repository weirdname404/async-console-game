from itertools import cycle
from core.event_loop import Sleep
from utils.curses_tools import (
    get_frame_size, read_controls, clean_draw
)
from config import SPACESHIP_SPEED

with open('animations/spaceship/rocket_frame_1.txt', 'r') as f:
    ROCKET_FRAME_1 = f.read()

with open('animations/spaceship/rocket_frame_2.txt', 'r') as f:
    ROCKET_FRAME_2 = f.read()

FRAME_ROWS, FRAME_COLS = get_frame_size(ROCKET_FRAME_1)


def _frame_generator():
    frames = cycle((ROCKET_FRAME_1, ROCKET_FRAME_2))
    while True:
        frame = next(frames)
        # animation should change every 2 tics
        for _ in range(2):
            yield frame


async def animate_spaceship(canvas, y, x):
    """
    Spaceship coroutine that handles player's input and draws frames.
    Works every step of event loop.
    """
    max_y, max_x = canvas.getmaxyx()
    max_y -= FRAME_ROWS
    max_x -= FRAME_COLS
    prev_frame = None
    frames = _frame_generator()

    while True:
        # get next frame
        frame = next(frames)
        # read controls
        dy, dx, space = read_controls(canvas)
        move = False
        # if there is any delta
        if dx or dy:
            x1 = x + dx * SPACESHIP_SPEED
            y1 = y + dy * SPACESHIP_SPEED
            # check borders intersection
            if max_x > x1 > 0 and max_y > y1 > 0:
                clean_draw(canvas, (x, y), (x1, y1), prev_frame, frame)
                x = x1
                y = y1
                move = True

        # if frame changed and there was no movement
        # delete prev frame and draw new one
        if frame is not prev_frame and not move:
            clean_draw(canvas, (x, y), (x, y), prev_frame, frame)

        await Sleep(0)
        prev_frame = frame
