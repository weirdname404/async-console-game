import curses
from utils import sleep
from _types import Animation


# (TICs, State)
STAR_ANIMATION: Animation = [
    (20, curses.A_DIM),
    (3, curses.A_NORMAL),
    (5, curses.A_BOLD),
    (3, curses.A_NORMAL)
]


async def draw_star(canvas, row: int, column: int, star: str, animation: Animation):
    while True:
        for ticks, state in animation:
            canvas.addstr(row, column, star, state)
            await sleep(ticks)
