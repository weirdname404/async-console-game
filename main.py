import time
import curses
import random
import config
from animations.star_animation import STAR_ANIMATION, draw_star
from utils import shift_animation, get_random_xy, Sleep


def main(canvas):
    canvas.border()
    curses.curs_set(False)
    coroutines = []
    animation_shifter = shift_animation(STAR_ANIMATION)

    for x, y in get_random_xy(*canvas.getmaxyx()):
        coroutines.append(
            draw_star(
                canvas=canvas,
                row=y,
                column=x,
                star=random.choice(config.STARS),
                animation=next(animation_shifter)
            )
        )

    start_event_loop(coroutines, canvas)


def start_event_loop(coroutines, canvas):
    while True:
        for c in coroutines:
            clock: Sleep = c.send(None)

        canvas.refresh()
        time.sleep(clock.seconds)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
