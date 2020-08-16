import random
import config
from _types import Coordinate
from typing import Generator


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and colums."""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])

    return rows, columns


def get_random_xy(max_y: int, max_x: int, density: float = None) -> Generator[Coordinate, None, None]:
    used_xy = set()
    density = config.STAR_DENSITY if density is None else density

    for _ in range(int(max_x * max_y * density)):
        x_y = random.randint(1, max_x - 2), random.randint(1, max_y - 2)

        if x_y in used_xy:
            continue

        used_xy.add(x_y)
        yield x_y
