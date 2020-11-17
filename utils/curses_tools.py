import random
import config
from core.types import Coordinate, Size
from typing import Iterator

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
            break

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas,
               start_x: int,
               start_y: int,
               text: str,
               negative: bool = False):
    """
    Draws multiline text fragment on canvas,
    erases text instead of drawing if negative=True is specified.
    """
    height, width = canvas.getmaxyx()

    for y, line in enumerate(text.splitlines(), round(start_y)):
        if y < 0:
            continue

        if y >= height:
            break

        for x, symbol in enumerate(line, round(start_x)):
            if x < 0:
                continue

            if x >= width:
                break

            if symbol == ' ':
                continue

            # Check that position is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if y == height - 1 and x == width - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(y, x, symbol)


def clean_draw(canvas, prev_xy, xy, prev_frame, frame, draw=True):
    '''deletes prev frame and draws new one'''
    x0, y0 = prev_xy
    x1, y1 = xy
    if prev_frame:
        draw_frame(canvas, x0, y0, prev_frame, negative=True)
    if draw:
        draw_frame(canvas, x1, y1, frame)


def get_frame_size(text: str) -> Size:
    """
    Calculates size of multiline text fragment,
    returns pair — number of rows and colums.
    """

    lines = text.splitlines()
    height = len(lines)
    width = max([len(line) for line in lines])

    return width, height


def get_random_coordinate(max_x: int,
                          max_y: int,
                          density: float = None) -> Iterator[Coordinate]:

    used_xy = set()
    density = config.STAR_DENSITY if density is None else density

    for _ in range(int(max_x * max_y * density)):
        x_y = random.randint(1, max_x - 2), random.randint(1, max_y - 2)

        if x_y in used_xy:
            continue

        used_xy.add(x_y)
        yield x_y
