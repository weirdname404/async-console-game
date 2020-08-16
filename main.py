import time
import curses
import random
import config
from animations.star_animation import STAR_ANIMATION, draw_star
from animations.fire_animation import fire
from utils import shift_animation
from utils.playscreen import get_random_xy
from utils.event_loop import Sleep


def main(canvas):
    canvas.border()
    curses.curs_set(False)
    coroutines = []
    animation_shifter = shift_animation(STAR_ANIMATION)
    max_y, max_x = canvas.getmaxyx()

    for x, y in get_random_xy(max_y, max_x):
        coroutines.append(
            draw_star(
                canvas=canvas,
                row=y,
                column=x,
                star=random.choice(config.STARS),
                animation=next(animation_shifter)
            )
        )

    # add single fire animation
    coroutines.append(
        fire(
            canvas=canvas,
            start_row=max_y - 2,
            start_column=max_x // 2
        )
    )

    start_event_loop(coroutines, canvas)


def start_event_loop(coroutines, canvas):
    while True:
        for i in range(len(coroutines)):
            try:
                clock: Sleep = coroutines[i].send(None)
            # coroutine was exhausted
            except (StopIteration, RuntimeError):
                coroutines = coroutines[:i] + coroutines[i + 1:]

        canvas.refresh()
        time.sleep(clock.seconds)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
