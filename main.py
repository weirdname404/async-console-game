import time
import curses
import asyncio
import random


# ANIMATIONS = {
#     'star': (
#         (2, curses.A_DIM),
#         (0.3, curses.A_NORMAL),
#         (0.5, curses.A_BOLD),
#         (0.3, curses.A_NORMAL)
#     )
# }

TIC_TIMEOUT = 0.1
STARS = '+*.:'

ANIMATION_INTERVAL = {
    'star': (2, 0.3, 0.5, 0.3)
}

ANIMATION_STEP = {
    'star': (
        curses.A_DIM,
        curses.A_NORMAL,
        curses.A_BOLD,
        curses.A_NORMAL
    )
}


async def draw_star(canvas, row, column, symbol='*'):
    # coroutine will never be exhausted
    while True:
        for step in ANIMATION_STEP['star']:
            canvas.addstr(row, column, symbol, step)
            await asyncio.sleep(0)


def main(canvas):
    canvas.border()
    curses.curs_set(False)
    coroutines = []
    for x, y in get_random_xy(*canvas.getmaxyx()):
        coroutines.append(
            draw_star(canvas, y, x, random.choice(STARS))
        )

    start_event_loop(coroutines, canvas)


def get_random_xy(max_y, max_x, density=0.1):
    used_xy = set()

    for _ in range(int(max_x * max_y * density)):
        x_y = random.randint(1, max_x - 2), random.randint(1, max_y - 2)

        if x_y in used_xy:
            continue

        used_xy.add(x_y)
        yield x_y


def start_event_loop(coroutines, canvas):
    while True:
        for t in ANIMATION_INTERVAL['star']:
            for c in coroutines:
                c.send(None)
            canvas.refresh()
            time.sleep(t)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
