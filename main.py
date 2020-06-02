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


# def draw_star_animation(canvas, y, x, star):
#     for state in ANIMATIONS['star']:
#         t, style = state
#         canvas.addstr(y, x, star, style)
#         canvas.refresh()
#         time.sleep(t)


async def blink(canvas, row, column, symbol='*'):
    # coroutine will never be exhausted
    while True:
        for step in ANIMATION_STEP['star']:
            canvas.addstr(row, column, symbol, step)
            await asyncio.sleep(0)


def main(canvas):
    canvas.border()
    curses.curs_set(False)

    start_pos = [50, 3]
    coroutines = []
    for _ in range(50):
        x, y = start_pos
        coroutines.append(blink(canvas, y, x, '*'))
        start_pos[random.choice((0, 1,))] += 1

    while True:
        for t in ANIMATION_INTERVAL['star']:
            for c in coroutines:
                c.send(None)
            canvas.refresh()
            time.sleep(t)
        # draw_star_animation(canvas, 5, 20, "*")


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)