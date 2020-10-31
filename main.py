import curses
import random
import config
from core.events import fill_orbit_with_garbage
from animations.star_animation import STAR_ANIMATION, animate_star
from animations.spaceship.animation import (
    animate_spaceship, FRAME_HEIGHT
)
from core.controller import run_spaceship
from core.event_loop import GameLoop
from core.obstacles import show_obstacles
from utils import shift_animation
from utils.curses_tools import get_random_coordinate


def main(canvas):
    canvas.nodelay(1)
    curses.curs_set(False)
    height, width = canvas.getmaxyx()
    max_y, max_x = height - 1, width - 1
    canvas_center = max_x // 2
    spaceship_x = canvas_center
    spaceship_y = max_y - FRAME_HEIGHT - config.START_Y_DELTA

    animation_shifter = shift_animation(STAR_ANIMATION)
    coroutines = []
    for x, y in get_random_coordinate(max_x, max_y):
        coroutines.append(
            animate_star(
                canvas=canvas,
                pos=(x, y),
                star=random.choice(config.STARS),
                animation=next(animation_shifter)
            )
        )

    coroutines.extend(
        [
            animate_spaceship(),
            run_spaceship(canvas=canvas, x=spaceship_x, y=spaceship_y),
            fill_orbit_with_garbage(canvas),
        ]
    )

    if config.DEBUG:
        coroutines.append(show_obstacles(canvas))

    GameLoop(coroutines, canvas).start()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
