import curses
import random
import config
from animations.star_animation import STAR_ANIMATION, animate_star
from animations.fire_animation import animate_gunshot
from animations.spaceship.animation import animate_spaceship
from core.event_loop import game_event_loop
from utils import shift_animation
from utils.curses_tools import get_random_coordinate


def main(canvas):
    canvas.border()
    canvas.nodelay(1)
    curses.curs_set(False)
    coroutines = []
    animation_shifter = shift_animation(STAR_ANIMATION)
    max_y, max_x = canvas.getmaxyx()

    for x, y in get_random_coordinate(max_y, max_x):
        coroutines.append(
            animate_star(
                canvas=canvas,
                row=y,
                column=x,
                star=random.choice(config.STARS),
                animation=next(animation_shifter)
            )
        )

    # add single fire animation
    dynamic_coroutines = [
        animate_gunshot(
            canvas=canvas,
            y=max_y - 11,
            x=max_x // 2 + 2
        )
    ]

    game_event_loop(
        static_coroutines=coroutines,
        dynamic_coroutines=dynamic_coroutines,
        spaceship_coroutine=animate_spaceship,
        canvas=canvas
    )


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
