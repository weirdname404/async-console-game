from itertools import cycle
from core.event_loop import Sleep
from game_types import Animation
from utils.curses_tools import (
    get_frame_size, read_controls, clean_draw
)
from config import SPACESHIP_SPEED

with open('animations/spaceship/rocket_frame_1.txt', 'r') as f:
    ROCKET_FRAME_1 = f.read()

with open('animations/spaceship/rocket_frame_2.txt', 'r') as f:
    ROCKET_FRAME_2 = f.read()

SPACESHIP_ANIMATION: Animation = (
    (2, ROCKET_FRAME_1),
    (2, ROCKET_FRAME_2)
)
FRAME_HEIGHT, FRAME_WIDTH = get_frame_size(ROCKET_FRAME_1)


def _frame_generator():
    frames = cycle(SPACESHIP_ANIMATION)
    while True:
        tics, frame = next(frames)
        # animation should change every 2 tics
        for _ in range(tics):
            yield frame


async def animate_spaceship(canvas, y, x):
    """
    Spaceship coroutine that handles player's input and draws frames.
    Works every step of event loop.
    """
    # getmaxyx() return height and width of the window.
    height, width = canvas.getmaxyx()
    # we want to stop the spaceship right before the border line
    max_y = height - FRAME_HEIGHT - 1
    max_x = width - FRAME_WIDTH - 1
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
            # count next coordinate
            x1 = x + dx * SPACESHIP_SPEED
            y1 = y + dy * SPACESHIP_SPEED
            # check borders intersection
            # choose closest point to the border
            x1 = max(1, min(x1, max_x))
            y1 = max(1, min(y1, max_y))
            # clean prev frame at old pos and draw current frame at new pos
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
