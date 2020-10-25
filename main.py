import curses
import random
import config
from animations.garbage.space_garbage import fill_orbit_with_garbage
from animations.star_animation import STAR_ANIMATION, animate_star
from animations.spaceship.animation import (
    animate_spaceship, FRAME_HEIGHT
)
from core.event_loop import GameLoop
from utils import shift_animation
from utils.curses_tools import get_random_coordinate


def main(canvas):
    canvas.nodelay(1)
    curses.curs_set(False)
    height, width = canvas.getmaxyx()
    max_y, max_x = height - 1, width - 1
    canvas_center = max_x // 2
    spaceship_x = canvas_center
    spaceship_y = max_y - FRAME_HEIGHT - config.SPACESHIP_SPEED

    animation_shifter = shift_animation(STAR_ANIMATION)
    coroutines = []
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

    coroutines.extend(
        [
            # add spaceship
            animate_spaceship(canvas=canvas, x=spaceship_x, y=spaceship_y),
            fill_orbit_with_garbage(canvas)
        ]
    )

    GameLoop(coroutines, canvas).start()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
